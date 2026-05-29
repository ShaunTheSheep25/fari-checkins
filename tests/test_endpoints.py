from fastapi.testclient import TestClient


def test_create_resident(client: TestClient) -> None:
    payload = {"name": "John", "address": "56 Square Street", "number": "3975916395"}
    response = client.post("/residents/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John"
    assert data["address"] == "56 Square Street"
    assert "id" in data


def test_get_residents(client: TestClient) -> None:
    response = client.get("/residents/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_resident_by_id(client: TestClient) -> None:
    payload = {"name": "John", "address": "56 Square Street", "number": "3975916395"}
    response = client.post("/residents/", json=payload)
    res_id = response.json()["id"]
    new_res = client.get(f"/residents/{res_id}")
    assert new_res.status_code == 200
    data = new_res.json()
    assert data["name"] == "John"


def test_update_resident(client: TestClient) -> None:
    payload = {"name": "John", "address": "56 Square Street", "number": "3975916395"}
    response = client.post("/residents/", json=payload)
    res_id = response.json()["id"]
    payload2 = {
        "name": "Alex",
        "address": "123 Cornelia Street",
        "number": "8989852476",
    }
    response2 = client.put(f"/residents/{res_id}", json=payload2)
    assert response2.status_code == 200
    data = response2.json()
    assert data["name"] == "Alex"
    assert data["address"] == "123 Cornelia Street"


def test_delete_resident(client: TestClient) -> None:
    payload = {"name": "John", "address": "56 Square Street", "number": "3975916395"}
    response = client.post("/residents/", json=payload)
    res_id = response.json()["id"]
    response2 = client.delete(f"/residents/{res_id}")
    assert response2.status_code == 200
    data = response2.json()
    assert data == {"message": "Resident successfully deleted."}
    response3 = client.get(f"/residents/{res_id}")
    assert response3.status_code == 404


def test_get_nonexistent_resident(client: TestClient) -> None:
    response = client.get("/residents/10001")
    assert response.status_code == 404
    assert response.json()["detail"] == "Resident not found."


def test_update_nonexistent_resident(client: TestClient) -> None:
    payload = {"name": "John", "address": "56 Square Street", "number": "3975916395"}
    response = client.put("/residents/10001", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Resident not found."


def test_delete_nonexistent_resident(client: TestClient) -> None:
    response = client.delete("/residents/10001")
    assert response.status_code == 404
    assert response.json()["detail"] == "Resident not found."


def test_missing_fields(client: TestClient) -> None:
    payload = {"name": "John"}
    response = client.post("/residents/", json=payload)
    assert response.status_code == 422


def test_create_checkin(client: TestClient) -> None:
    payload = {"name": "John", "address": "56 Square Street", "number": "3975916395"}
    response = client.post("/residents/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John"
    assert data["address"] == "56 Square Street"
    res_id = data["id"]
    payload2 = {"res_id": res_id, "mood": "happy", "category": "medical"}
    response2 = client.post("/checkins/", json=payload2)
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["res_id"] == res_id
    assert data2["mood"] == "happy"


def test_get_checkins_for_resident(client: TestClient) -> None:
    res_payload = {
        "name": "John",
        "address": "56 Square Street",
        "number": "3975916395",
    }
    res_response = client.post("/residents/", json=res_payload)
    res_id = res_response.json()["id"]
    ck1 = {"res_id": res_id, "mood": "happy", "category": "medical"}
    ck2 = {"res_id": res_id, "mood": "anxious", "category": "social"}
    client.post("/checkins/", json=ck1)
    client.post("/checkins/", json=ck2)
    response = client.get(f"/checkins/resident/{res_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["mood"] == "happy"
    assert data[1]["mood"] == "anxious"


def test_get_n_checkins(client: TestClient) -> None:
    res_payload = {
        "name": "John",
        "address": "56 Square Street",
        "number": "3975916395",
    }
    res_response = client.post("/residents/", json=res_payload)
    res_id = res_response.json()["id"]
    moods = ["happy", "sad", "anxious", "happy", "sad"]
    for mood in moods:
        client.post(
            "/checkins/", json={"res_id": res_id, "mood": mood, "category": "medical"}
        )
    response = client.get(f"/checkins/resident/{res_id}/recent?n=3")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_get_summary(client: TestClient) -> None:
    res_payload = {
        "name": "John",
        "address": "56 Square Street",
        "number": "3975916395",
    }
    res_response = client.post("/residents/", json=res_payload)
    res_id = res_response.json()["id"]
    moods = ["happy", "sad", "anxious", "happy", "sad", "happy"]
    categories = ["medical", "social", "medical", "social", "medical", "medical"]
    for i in range(6):
        client.post(
            "/checkins/",
            json={"res_id": res_id, "mood": moods[i], "category": categories[i]},
        )
    response = client.get(f"/checkins/summary/{res_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["resident_id"] == res_id
    assert data["by_mood"]["happy"] == 3
    assert data["by_mood"]["sad"] == 2
    assert data["by_mood"]["anxious"] == 1
    assert data["by_category"]["medical"] == 4
    assert data["by_category"]["social"] == 2


def test_post_checkin_nonexistent(client: TestClient) -> None:
    payload = {"res_id": "10001", "mood": "happy", "category": "medical"}
    response = client.post("/checkins/", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Resident not found."


def test_get_checkins_nonexistent(client: TestClient) -> None:
    response = client.get("/checkins/resident/10001")
    assert response.status_code == 404
    assert response.json()["detail"] == "Resident not found."
