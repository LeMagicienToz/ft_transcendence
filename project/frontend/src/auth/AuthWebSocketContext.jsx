
import React, { createContext, useContext, useEffect, useState } from 'react';

const AuthWebSocketContext = createContext(null);

export const WebSocketProvider = ({ children }) => {
    const [socket, setSocket] = useState(null);
    const [friends, setFriends] = useState([]);

    useEffect(() => {
        const socket = new WebSocket('ws://localhost:8000/ws/user_connection/');
        setSocket(socket);

        socket.onopen = () => {
            console.log('WebSocket connected');
        };

        socket.onmessage = (event) => {
            console.log('Message received:', event.data);
            const message = JSON.parse(event.data);
            if (message.user_id && message.status)
                updateFriendStatus(message.user_id, message.status);

        };

        socket.onclose = () => {
            console.log('WebSocket closed'); // est ce que je redirige vers la page de login ?
        };

        return () => {
            socket.close(); // detecte fermeture onglet/fenetre sur l'ensemble de l'app
        };
    }, []);

    const updateFriendStatus = (userId, status) => {
            const updatedFriends = friends.map((friend) => {
                if (friend.id === userId) {
                    return { ...friend, status };
                }
                return friend;
            });
            setFriends(updatedFriends);
        };


    // Fonction pour gérer la déconnexion propre
    const WebSocketHandleLogout = () => {
        if (socket) {
            socket.close();
            console.log('Déconnecté et WebSocket fermé');
        }
    };

    return (
        <AuthWebSocketContext.Provider value={{ socket, friends, sendMessage, WebSocketHandleLogout }}>
            {children}
        </AuthWebSocketContext.Provider>
    );
};


export { AuthWebSocketContext };