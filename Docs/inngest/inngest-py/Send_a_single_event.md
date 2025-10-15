await inngest_client.send(inngest.Event(
    name="app/user.created", 
    data={"user_id": 123, "name": "Jane"}
))