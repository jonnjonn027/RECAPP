window.addEventListener('load',function() {
	document.getElementById('submitbutton').addEventListener('click', function() {
		var firstName = document.getElementById('firstName')
		var middleName = document.getElementById('middleName')
		var lastName = document.getElementById('lastName')
		var domain = document.getElementById('domain') 
		var permutations = getPermutations(firstName, middleName, lastName, domain);
	});
});

function getPermutations(firstName, middleName, lastName, domain) {
	/* Returns all of the desired permutations for the given data */

	// Extract the needed variables
	var firstInitial = firstName[0]
	
	// This list is incomplete, but should be sufficient to get started
	var permutationTemplates = [
		'{fn}',
		'{ln}',
		'{fn}{ln}',
		'{fn}.{ln}',
		'{fi}{ln}'
	]

	// for each permutation template
	for (var i=0;i<permutationTemplates.length;i++) {
		// grab the permutation
		var permutation = permutationTemplates[i];

		// apply the replacements
		permutation = permutation
			.replace("{fn}",firstName)
			.replace("{ln}",lastName)
			.replace("{mn}",middleName)
			.replace("{fi}",firstInitial)

		// append the domain
		permutation = permutation + "@" + domain

	  // print it to the console 
		// (you can see the console by right clicking the popup and clicking "Inspect Popup"
		// Then, in the top right, click the "Console" tab
		// In the real version we'll do something different with this 
		console.log(permutation)
	}
	
}
