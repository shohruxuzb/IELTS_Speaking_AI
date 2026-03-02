@app.get("/generate-part1")
async def generate_part1():
    return generate_part1_questions()

@app.get("/generate-part2")
async def generate_part2():
    return generate_part2_question()

@app.get("/generate-part3")
async def generate_part3():
    return generate_part3_questions()

