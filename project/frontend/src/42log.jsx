import React from 'react';

const Code_sender = () => {
		// const navigate = useNavigate();
		const client_id = "u-s4t2ud-5f229ec68009f569b5bbe50029109f47ac0c5676791b1eb10efb0d8b8b99fe6c";
		const client_secret = "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"
	
		try {
			const response = fetch('https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-583f55ae418416d61ca305bc374aa0ea166d67420ca068fcda962a14894fc200&redirect_uri=https%3A%2F%2Flocalhost%3A8443%2Fapi%2Fauth%2Fcallback%2F42%2F&response_type=code', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(
					{
						"grant_type": "client_credentials",
						"client_id": client_id,
						"client_secret": client_secret
					}),
			});

			if (response.ok) {
				const data = response.json();
				setUserData(data); // Ici, vous pouvez récupérer user_id, user_name et image_url
				console.log(data);
				navigate('/Home');
			} else {
				console.log("errorData");
			}
		}catch (err) {
			setError('Une erreur s\'est produite');
		}
		return (
			<h1>
				dwadwa
			</h1>
		)
};

export default Code_sender;