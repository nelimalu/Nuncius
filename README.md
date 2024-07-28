# Nuncius
end-to-end encrypted command-line messenger

## ⚡inspiration
This project is inspired by the Vox messaging system in Want by Cindy Pon, that was used by the revolutionaries to communicate discreetly.

## 🛠️ functionality
 - SHA256 encrypted login
 - Unlimited (in theory) user chatroom
 - All messages are end-to-end encrypted using RSA, as well as a diffie-hellman exchange to prevent man-in-the-middle attacks
 - Historical messages are saved on the client, new chatroom members will not be able to see previous messages

##
also note that users have to be manually added in the users.json file in the server directory, so theres no account creation, which is great for private conversations
