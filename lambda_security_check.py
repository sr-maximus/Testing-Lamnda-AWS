import boto3
import json

# Inicializar clientes de AWS
lambda_client = boto3.client('lambda')
iam_client = boto3.client('iam')

def check_lambda_functions():
    functions = lambda_client.list_functions()['Functions']
    for function in functions:
        function_name = function['FunctionName']
        print(f"\nChecking Lambda function: {function_name}")

        # Obtener detalles de la función
        function_config = lambda_client.get_function_configuration(FunctionName=function_name)
        role_arn = function_config['Role']
        handler = function_config['Handler']
        runtime = function_config['Runtime']
        environment_vars = function_config.get('Environment', {}).get('Variables', {})
        vpc_config = function_config.get('VpcConfig', {})
        code_size = function_config.get('CodeSize', 'Unknown')

        # Verificar el rol y sus políticas
        role_name = role_arn.split('/')[-1]
        role = iam_client.get_role(RoleName=role_name)['Role']
        policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
        print(f"Role: {role_name}")
        print(f"Policies: {[policy['PolicyName'] for policy in policies]}")

        # Verificar permisos de políticas del rol
        for policy in policies:
            policy_arn = policy['PolicyArn']
            policy_document = iam_client.get_policy_version(
                PolicyArn=policy_arn,
                VersionId=iam_client.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
            )['PolicyVersion']['Document']
            print(f"Policy Document for {policy_arn}: {json.dumps(policy_document, indent=2)}")

            # Evaluar si las políticas siguen el principio de menor privilegio
            if not is_minimum_permission(policy_document):
                print(f"Warning: Policy {policy_arn} may not follow the principle of least privilege.")

        # Verificar la configuración de la función
        print(f"Handler: {handler}")
        print(f"Runtime: {runtime}")
        print(f"Environment Variables: {sanitize_environment_vars(environment_vars)}")
        print(f"VPC Config: {vpc_config}")
        print(f"Code Size: {code_size} bytes")

        # Verificar configuraciones de versión de Lambda
        versions = lambda_client.list_versions_by_function(FunctionName=function_name)['Versions']
        print(f"Versions: {[version['Version'] for version in versions]}")

        # Verificar configuración de alias
        aliases = lambda_client.list_aliases(FunctionName=function_name)['Aliases']
        print(f"Aliases: {[alias['Name'] for alias in aliases]}")

        # Verificar la configuración de invocaciones de función
        permissions = lambda_client.list_event_source_mappings(FunctionName=function_name)['EventSourceMappings']
        print(f"Event Source Mappings: {[mapping['EventSourceArn'] for mapping in permissions]}")

        # Verificar la política de acceso de la función
        try:
            policy = lambda_client.get_policy(FunctionName=function_name)['Policy']
            print(f"Function Policy: {policy}")
        except lambda_client.exceptions.ResourceNotFoundException:
            print("No access policy found for this function.")

def is_minimum_permission(policy_document):
    # Implementar lógica para evaluar si la política sigue el principio de menor privilegio
    # Esto puede incluir verificar los permisos de acción y recursos en el documento
    return True  # Placeholder, implementar lógica real aquí

def sanitize_environment_vars(vars):
    # Implementar lógica para sanitizar variables de entorno
    # Esto puede incluir verificar si hay valores sensibles expuestos
    sanitized_vars = {}
    for key, value in vars.items():
        if 'PASSWORD' in key.upper() or 'SECRET' in key.upper():
            sanitized_vars[key] = '[REDACTED]'
        else:
            sanitized_vars[key] = value
    return sanitized_vars

if __name__ == "__main__":
    check_lambda_functions()
