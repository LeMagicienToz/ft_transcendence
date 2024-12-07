import React from 'react';

import { useToast } from '../../contexts/ToastContext';

import BaseForm from './BaseForm';
import BaseButton from '../Buttons/BaseButton';
import PasswordInput from '../Inputs/PasswordInput';
import SelectInput from '../Inputs/SelectInput';

import './TwoFactorUpdateForm.css'

const TwoFactorUpdateForm = ({ onSuccess = () => {}, onFailure = () => {}, disabled = false }) => {

    const { addToast } = useToast();

    const handleValidation = (form) => {
        let valid = true;

        if (!/^(true|false)$/.test(form.TwoFA_enabled.value)) {
            addToast('An error has occured.', 'failure', 10000)
            valid = false;
        }
        return valid;
    }

    const handleFailure = (json) => {
    }

    const handleSuccess = (json) => {
        addToast('2FA updated successfully.', 'success', 5000);
    }

    return (
        <BaseForm
            handleValidation={handleValidation}
            onSuccess={(json) => {handleSuccess(json); onSuccess(json)}}
            onFailure={(json) => {handleFailure(json); onFailure(json)}}
            target='/api/auth/me/update_twofa_status/'
            type='json'
            headers={{'Content-Type': 'application/json'}}
            disabled={disabled}
        >
            <SelectInput
                id='twoFA_enabled'
                name='TwoFA_enabled'
                label='Enable 2FA'
                options={[{label: 'Enabled', value: 'True'}, {label: 'Disabled', value: 'False'}]}
            />
            <BaseButton text='Update 2FA' className='primary' />
        </BaseForm>
    );
}

export default TwoFactorUpdateForm;
