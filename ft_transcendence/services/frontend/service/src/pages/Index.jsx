import React, { useState } from 'react';

import BaseButton from '../components/Buttons/BaseButton';
import LinkButton from '../components/Buttons/LinkButton';
import LoginWindow from '../components/Windows/LoginWindow';
import SpaceBackground from '../components/SpaceBackground';
import Typewriter from '../components/Typewriter';

import './Index.css'

const Index = () => {
    const [loginWindowState, setLoginWindowState] = useState(false);

    const authorizeURL = new URL("https://api.intra.42.fr/oauth/authorize");
	authorizeURL.searchParams.append("client_id", "u-s4t2ud-0fb37f903a509ffef7fef8a465a0d364fd68770a44139adc8a756ee25376f128")
	authorizeURL.searchParams.append("redirect_uri", `https://${window.location.host}/api/auth/callback/42/`)
	authorizeURL.searchParams.append("response_type", "code")

	return (
        <div className={`page`} id={`page-index`}>
            <SpaceBackground />
            <section className={`view`}>
                <LoginWindow onClose={() => setLoginWindowState(false)} isOpen={loginWindowState} />
                <div className={`wrapper`}>
                    <Typewriter text='ft_transendence' />
                    <nav>
                        <BaseButton onClick={() => setLoginWindowState(true)} text='JOIN THE GAME' className='space' />
                        <LinkButton route={authorizeURL} text='LOGIN WITH 42' className='space' />
                    </nav>
                </div>
            </section>
        </div>
	);
}

export default Index
