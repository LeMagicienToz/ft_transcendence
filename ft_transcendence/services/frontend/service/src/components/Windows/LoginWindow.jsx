import React from 'react';

import BaseWindow from './BaseWindow';
import LoginForm from '../Forms/LoginForm';
import RegisterForm from '../Forms/RegisterForm';
import Tab from '../Tabs/Tab';
import Tabs from '../Tabs/Tabs';

import './LoginWindow.css';

const LoginWindow = ({ onClose = () => {}, isOpen = false, title = 'Join the game !', height = '635px', width = '500px' }) => {

    return (
        <BaseWindow
            onClose={onClose}
            isOpen={isOpen}
            title={title}
            height={height}
            width={width}
        >
            <Tabs>
                <Tab name='Login' >
                    <LoginForm />
                </Tab>
                <Tab name='Register' >
                    <RegisterForm />
                </Tab>
            </Tabs>
        </BaseWindow>
    );
}

export default LoginWindow;
