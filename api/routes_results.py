@app.post("/aggregate-results")
async def aggregate_results(req: EvaluationsRequest):
    """
    Takes a list of JSON evaluations for Part 1, Part 2, and Part 3
    and returns a weighted overall IELTS band report.
    """
    return aggregate_evaluations(req.evaluations)

