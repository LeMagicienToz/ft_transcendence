import MyButton from "../Theme/MyButton";
import "./Profile.css"
import React, { useState, useEffect } from 'react';

const Profile = () => {
	const [userData, setUserData] = useState(null);
	const [error, setError] = useState(null);
	const [isNormal, setIsNormal] = useState(true);

	useEffect(() => {
		const getUserData = async () => {
			try {
				const data = await fetchUserData();
				setUserData(data);
				// Définir `isNormal` une fois que `userData` est récupéré
				if (data && data.username.endsWith("#42")) {
					setIsNormal(false);
				}
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
					<h1>{userData ? userData.username : "Loading ..."}</h1>
				)}
				{isNormal ? (
					<NormalUserForm />
				) : (
					<FortytwoUserForm username={userData.username}/>
				)}
			</div>
			<div className="container-avatar">
				<MyButton text="Change avatar" to="avatar" />
			</div>
		</div>
	);
};


const NormalUserForm = () => {
	const [username, setUserName] = useState('');
	const [new_password, setPassword] = useState('');
	const [email, setEmail] = useState('');
	const [twoFA_enabled, setTwoFAEnabled] = useState(false);
	const [userData, setUserData] = useState(null);
	const [error, setError] = useState('');

	const handleNormal = async () => {
		try {
			const response = await fetch('https://localhost:8443/api/auth/set_profile/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ username, email, twoFA_enabled, new_password}),
				credentials: 'include',
			});
			if (response.ok) {
				const data = await response.json();
				console.log("OOOOOOOOOOKKKKKKKKKKKKKK");
				setUserData(data);
			} else {
				const errorData = await response.json();
				setError(errorData.error);
				console.log("dwajdiwajdoiwa");
			}
		} catch (err) {
			setError('Une erreur s\'est produite');
		}
	};	

return (
	<>
		<div className="form-nuser">
			<form>
					<label className="label-profile" htmlFor="exampleInputUsername1">UserName </label>
					<input
						type="username"
						className="case-input"
						username="exampleInputUsername1"
						placeholder="UserName"
						value={username}
						onChange={(e) => setUserName(e.target.value)}
						/>
					<label className="label-profile" htmlFor="exampleInputEmail1">Email address </label>
							<input
								type="email"
								className="case-input"
								id="exampleInputEmail1"
								placeholder="Enter email"
								value={email}
								onChange={(e) => setEmail(e.target.value)}
							/>
					<label className="label-profile" htmlFor="exampleInputPassword1">new_password </label>
					<input
						type="password"
						className="case-input"
						id="exampleInputPassword1"
						placeholder="Password"
						value={new_password}
						onChange={(e) => setPassword(e.target.value)}
						/>
					<div style={{ marginTop: "20px" }}>
						<MyButton text="Save and Quit" onClick={handleNormal}/>
					</div>
			</form>
		</div>
	</>

);
}

const FortytwoUserForm = ({username}) => {
	return (
			<>
					<div className="form-nuser">
						<h2>You can't change 42 User Information</h2>
					<form>
						<label className="label-profile" htmlFor="exampleInputUsername1">UserName </label>
						<input
							type="text"
							className="case-input read-only"
							id="exampleInputUsername1"
							placeholder={username}
							readOnly
						/>

						<label className="label-profile" htmlFor="exampleInputEmail1">Email address </label>
						<input
							type="email"
							className="case-input read-only"
							id="exampleInputEmail1"
							placeholder="Undefined"
							readOnly
						/>

						<label className="label-profile" htmlFor="exampleInputPassword1">Password </label>
						<input
							type="password"
							className="case-input read-only"
							id="exampleInputPassword1"
							placeholder="***********"
							readOnly
						/>

						<div style={{ marginTop: "20px" }}>
							<MyButton text="Quit" to="homepage"/>
						</div>
					</form>
				</div>
			</>
	);

}

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

export default Profile