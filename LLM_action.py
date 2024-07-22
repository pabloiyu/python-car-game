import base64

def _encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def make_llm_move_car(llm_client, image_path):
    
    system_prompt = """ You are an AI controlling a red car in a video game. Your goal is to avoid collisions and maximize your score. Rules:

    - The red car is at the bottom of the screen and moves upward.
    - You should avoid the other yellow cars on the road. They move downward.
    - The road has three lanes. You can move left, right, or stay in your lane. If you are in the leftmost lane, you can either stay or move right. If you are in the rightmost lane, you can either stay or move left. 
    - Avoid lanes with vehicles directly ahead (same lane, further up). Be proactive and change lanes in advance.
    - Don't change into adjacent lanes if there are other vehicles parallel or close to the red car.
    - Look ahead and be proactive in decision making. If the red car in in the right lane and there is a vehicle directly ahead in the right lane, you should move left to avoid it for example. 
    - However, only change lanes when necessary to avoid collisions. Thus, your common response should be "stay", unless it is necessary to change lanes to avoid collision.
    - Respond with only: "left", "right", "stay".
    """
    # Getting the base64 string
    base64_image = _encode_image(image_path)
    
    # Initial message with the image
    message_history = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high" 
                    },
                },
            ],
        }
    ]
    
    # Make the API call
    response = llm_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message_history,
        max_tokens=4,
    )

    # Get the assistant's response
    assistant_response = response.choices[0].message.content
    print(assistant_response)
    
    return assistant_response