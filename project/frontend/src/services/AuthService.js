export class AuthService {


	constructor() {
		this.backendApi = 'http://localhost:8443/api/';
	}


	// Méthode d'enregistrement
	register(data) {
		return fetch(this.backendApi + 'register/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(data),
		})
		.then(response => response.json())
		.then(data => {
			console.log('Success:', data);
			// Part pour gérer la réponse du backend
		})
		.catch((error) => {
			console.error('Error:', error);
		});
	}

	// Méthode de déconnexion
	logout() {
	    return fetch(this.backendApi + 'logout/', {
	        method: 'POST',
	        headers: {
	            'Content-Type': 'application/json',
	        },
	    })
	    .then(response => response.json())
	    .then(data => {
	        console.log('Logout Success:', data);
	    })
	    .catch((error) => {
	        console.error('Logout Error:', error);
	    });
	}

	// Méthode de connexion
	login(data) {
	    return fetch(this.backendApi + 'login/', {
	        method: 'POST',
	        headers: {
	            'Content-Type': 'application/json',
	        },
	        body: JSON.stringify(data),
	    })
	    .then(response => response.json())
	    .then(data => {
	        console.log('Login Success:', data);
	        // Part pour gérer la réponse du backend
	    })
	    .catch((error) => {
	        console.error('Login Error:', error);
	    });
	}

	// Vérification de l'autorité
	checkAuthority() {
	    // Logique de vérification de l'autorité
	    return true;
	}
}
