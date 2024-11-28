import runpod
import time

def process_input(input):
    """
    Execute the application code
    """
    name = input['name']
    greeting = f'Hello {name}'

    return {
        "greeting": greeting
    }


# ---------------------------------------------------------------------------- #
#                                RunPod Handler                                #
# ---------------------------------------------------------------------------- #
def handler(event):
    """
    This is the handler function that will be called by RunPod serverless.
    """
    return process_input(event['input'])

# def handler(event):
#     input = event['input']
#     instruction = input.get('instruction')
#     seconds = input.get('seconds', 0)

#     # Placeholder for a task; replace with image or text generation logic as needed
#     time.sleep(seconds)
#     result = instruction.replace(instruction.split()[0], 'created', 1)

#     return result

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
    