# Nuncius
end-to-end encrypted command-line messenger

## explanation
was kinda bored and found a youtube video (computerphile) about RSA encryption, and wanted to implement it myself.
this application uses RSA, but doesn't implement diffie-hellman key exchange so it's susceptible to a man in the middle attack
might add diffie hellman in the future if i feel like it

also note that users have to be manually added in the users.json file in the server directory, so theres no account creation, which is great for private conversations
