from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestGetSeriesContents:
    # Only Check Status Code
    def test_get_series_contents(self):
        response = client.get("/v1/series/1")
        assert response.status_code == 200

    # Check Response Value
    def test_get_series_contents_with_response_value(self):
        response = client.get("/v1/series/1")
        assert response.status_code == 200
        assert response.json() == {
          "id": 1,
          "title": "배고픈 개발자",
          "description": "배고픈 개발자의 푸념을 담았습니다.",
          "created_at": "2021-08-25T18:22:07",
          "paragraph_list": [
            {
              "text": "아! 배가고픈 인생이여",
              "id": 1
            },
            {
              "text": "우리 모두 힘을 내야한다!",
              "id": 2
            }
          ],
          "rating": 0
        }

    # Check if endpoint is incorrect
    def test_get_series_contents_bad_request(self, random_endpoint):
        response = client.get(f"/v1/series/{random_endpoint}")
        assert response.status_code == 404
