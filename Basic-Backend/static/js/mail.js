

function sendEmail() {
	Email.send({
	Host: "smtp.gmail.com",
	Username : document.getElementById("emailAddressFromInput").value,
	Password : document.getElementById("emailFromPass").value,
	To : document.getElementById("emailAddressToInput").value,
	From : "<sender’s email address>",
	Subject : document.getElementById("emailSubjectInput").value,
	Body : document.getElementById("emailContentInput").value,
	}).then(
		message => alert("mail sent successfully")
	);
}