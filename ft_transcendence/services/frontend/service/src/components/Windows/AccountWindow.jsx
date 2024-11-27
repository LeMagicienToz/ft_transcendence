import React from 'react';

import BaseWindow from './BaseWindow';
import DeleteAccoutButton from '../Buttons/DeleteAccoutButton';
import SecurityForm from '../Forms/SecurityForm';
import ProfileForm from '../Forms/ProfileForm';
import Tab from '../Tabs/Tab';
import Tabs from '../Tabs/Tabs';

import './AccountWindow.css';

const AccountWindow = ({ onClose = () => {}, isOpen = false, title = 'Account', height = '635px', width = '500px' }) => {

    return (
        <BaseWindow
            onClose={onClose}
            isOpen={isOpen}
            title={title}
            height={height}
            width={width}
            className='account'
        >
            <Tabs>
                <Tab name='Profile' >
                    <ProfileForm />
                </Tab>
                <Tab name='Security' >
                    <div className='col' >
                        <SecurityForm />
                        <DeleteAccoutButton />
                    </div>
                </Tab>
            </Tabs>
        </BaseWindow>
    );
}

export default AccountWindow;
