## Algorand Notes

### Description

This smart contract is a simple One-note or sticky notes simulation created using Pyteal. In the contract, users are enabled to interact with the contract by adding notes and deleting notes, and also liking or unliking the dApp, all while utilizing Algorand's global and local states for data storage and management. The app leverages Pyteal's capabilities to utilize global and local states for storing and managing important stack values.

### Globals

The contract uses one global which is likes, this stores and will be later on displayed for the users who likes the dApp

- global_likes - # uint64

### Locals

The contract allocates 15 local uint64s, one is for storing the user's own like on the dApp and the 14 remaining local uint64s will be used for storing notes. I use uint64 to store the notes where I put a value of Int(1) if the notes existed and store the actual content of the notes in the key of the uint64

- local_like - # uint64
- note - # key input uint64

### No_Op and Subroutines

The contract uses 4 no_op and subroutines, These are add_note, delete_note, like, and unlike.

- `add_note()`: This subroutine handles the logic for adding a note in the game. It checks if the user has opted-in to the game and then adds a note for the user by updating the local state. The transaction is approved after adding the note.
- `delete_note()`: This subroutine handles the logic for deleting a note in the game. It checks if the user has opted-in to the game and if the note exists for the user. If both conditions are met, the note is deleted from the local state. The transaction is approved after deleting the note.
- `like()`: This subroutine handles the logic for the "like" action in the game. It checks if the user has already liked the content and, if not, increases the global likes count and updates the local like count for the user. If the user has already liked the content, the transaction is rejected.
- `unLike()`: This subroutine handles the logic for the "unlike" action in the game. It checks if the user has already liked the content and, if so, decreases the global likes count and updates the local like count for the user. If the user hasn't liked the content, the transaction is rejected.

### Application ID

- `214948461`
- https://testnet.algoexplorer.io/application/214948461

## Frontend

Here's the [link](https://github.com/hiromero/algorand-notes) to the dApp's frontend repository.

## Demo

Here is a `video link TO BE UPDATED!!` that shows how the user interacted with the dApp.

![Alt text](demo%20img.PNG)

To test it out, click on this [demo link](https://algorand-notes.vercel.app/).
