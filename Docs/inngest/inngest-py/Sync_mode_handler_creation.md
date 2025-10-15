@app.route("/api/inngest", methods=["GET", "POST", "PUT"])
def inngest_api():
    comm_req = comm_lib.CommRequest(...)
    return handler.post_sync(comm_req)