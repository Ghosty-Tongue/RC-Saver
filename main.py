import requests
import json
from datetime import datetime

def load_cookies(cookie_file):
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    return cookies

def fetch_authenticated_user_id(cookies):
    url = "https://users.roblox.com/v1/users/authenticated"
    headers = {
        "Cookie": "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data['id']
        return user_id
    else:
        print(f"Failed to fetch authenticated user ID: {response.status_code} - {response.text}")
        return None

def fetch_all_usernames_with_display_names(cookies, authenticated_user_id):
    url = "https://apis.roblox.com/platform-chat-api/v1/get-user-conversations"
    headers = {
        "Cookie": "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    }
    params = {
        "include_user_data": "true",
        "pageSize": "500"
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        conversations_data = response.json()
        usernames_with_display_names = []
        if 'conversations' in conversations_data:
            conversations = conversations_data['conversations']
            for conv in conversations:
                first_user_data = next(iter(conv['user_data'].values()))  # Get data of the first user
                username = first_user_data['name']
                display_name = first_user_data['display_name']
                user_id = first_user_data['id']
                
                if user_id == authenticated_user_id:
                    continue
                
                usernames_with_display_names.append({
                    'username': username,
                    'display_name': display_name,
                    'conversation_id': conv['id']
                })
        
        return usernames_with_display_names
    else:
        print(f"Failed to fetch conversations: {response.status_code} - {response.text}")
        return None

def fetch_messages_from_conversation(cookies, conversation_id):
    url = f"https://apis.roblox.com/platform-chat-api/v1/get-conversation-messages"
    headers = {
        "Cookie": "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    }
    params = {
        "conversation_id": conversation_id,
        "pageSize": "500"
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        messages_data = response.json()
        if 'messages' in messages_data:
            messages = messages_data['messages']
            return messages
        else:
            print(f"No messages found for conversation ID: {conversation_id}")
            return []
    else:
        print(f"Failed to fetch messages: {response.status_code} - {response.text}")
        return []

def save_messages_to_file(username, messages, file_format='txt'):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{username}_messages_{timestamp}.{file_format}"
    
    if file_format == 'txt':
        with open(filename, 'w', encoding='utf-8') as f:
            for message in messages:
                f.write(f"{message['content']}\n")
        print(f"Messages saved to {filename}")
    
    elif file_format == 'html':
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("<html>\n<head>\n<title>Chat Messages</title>\n</head>\n<body>\n")
            f.write(f"<h1>Messages for {username}</h1>\n")
            f.write("<ul>\n")
            for message in messages:
                f.write(f"<li>{message['content']}</li>\n")
            f.write("</ul>\n</body>\n</html>")
        print(f"Messages saved to {filename}")
    
    else:
        print("Unsupported file format. Please choose 'txt' or 'html'.")

if __name__ == "__main__":
    cookie_file = r"C:\Users\home\Downloads\cookies.json"
    cookies = load_cookies(cookie_file)
    
    authenticated_user_id = fetch_authenticated_user_id(cookies)
    if authenticated_user_id:
        print(f"Authenticated user ID: {authenticated_user_id}")
        
        all_usernames_with_display_names = fetch_all_usernames_with_display_names(cookies, authenticated_user_id)
        if all_usernames_with_display_names:
            print("Select a username to fetch conversations:")
            for idx, user_info in enumerate(all_usernames_with_display_names, start=1):
                print(f"{idx}. {user_info['username']} ({user_info['display_name']})")
            
            while True:
                try:
                    user_selection = int(input("Enter the number of the username to fetch conversations: "))
                    if 1 <= user_selection <= len(all_usernames_with_display_names):
                        selected_user = all_usernames_with_display_names[user_selection - 1]
                        selected_username = selected_user['username']
                        selected_display_name = selected_user['display_name']
                        conversation_id = selected_user['conversation_id']
                        print(f"Selected username (display_name): {selected_username} ({selected_display_name})")
                        
                        messages = fetch_messages_from_conversation(cookies, conversation_id)
                        if messages:
                            messages.reverse()
                            
                            print(f"Messages in conversation {conversation_id}:")
                            for idx, message in enumerate(messages, start=1):
                                print(f"{idx}. {message['content']}")
                            
                            save_option = input("Do you want to save these messages? (y/n): ").strip().lower()
                            if save_option == 'y':
                                file_format = input("Enter 'txt' or 'html' to save as: ").strip().lower()
                                save_messages_to_file(selected_username, messages, file_format)
                            break
                        else:
                            print("Failed to fetch messages.")
                        break
                    else:
                        print("Invalid selection. Please enter a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            print("No conversations found.")
    else:
        print("Failed to fetch authenticated user ID.")
