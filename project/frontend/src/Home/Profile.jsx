import "./Profile.css"
import React, { useState, useEffect } from 'react';

const fetchUserData = async () => {
	try {
	  const response = await fetch('https://localhost:8443/api/auth/get_user/', {
		method: 'GET',
		headers: {
		  'Content-Type': 'application/json',
		},
		credentials: 'include'
	  });
  
	  if (response.ok) {
		const data = await response.json();
		return(data);
	  } else {
		  const errorData = await response.json();
		  console.log(errorData.error);
		}
	} catch (error) {
	  console.error("Erreur lors de la requête : ", error);
	  console.log("Une erreur est survenue");
	}
  };

const Profile = () => {
	const data=fetchUserData();

	const [userData, setUserData] = useState(null);
  	const [error, setError] = useState(null);

	useEffect(() => {
		const getUserData = async () => {
		try {
			const data = await fetchUserData();
			setUserData(data);
		} catch (error) {
			setError("Impossible de récupérer les données utilisateur");
		}
		};
		getUserData();
	  }, []);
	return (
		<div className="background">
			<div className="container-profile">
				{error ? (
					<h1>{error}</h1>
				) : (
					<h1>
					{userData ? userData.username : "Loading ..."}
					</h1>
				)}
			</div>
		</div>
	)
};

export default Profile