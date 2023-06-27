from components.controller.fastapi.main import create_component

# uvicorn does not interpret "component:create component()" correctly and will not invoke
# the create function like gunicorn will so this is needed for service-devel
component = create_component()
