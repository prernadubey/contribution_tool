def test_home_route__get_resource__hello_message_returned(fastapi_test_client):
    response = fastapi_test_client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to RD Compensation Tool backend service."
