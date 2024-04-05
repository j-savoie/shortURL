// register modal component
 Vue.component("modal", {
   template: "#modal-template"
 });

var app = new Vue({
  el: "#app",

  //------- data --------
  data: {
    serviceURL: "https://cs3103.cs.unb.ca:8028",
    authenticated: false,
    urlData: null,
    loggedIn: null,
    editModal: false,
    input: {
      username: "",
      password: "",
      addUrlData: "",
    },
    selectedURL: {
      language: "",
      level: "",
      name: "",
      province: "",
      schoolId: ""
    }
  },
  //------- lifecyle hooks --------
  /*mounted: function() {
    axios
    .get(this.serviceURL+"/signin")
    .then(response => {
      if (response.data.status == "success") {
        this.authenticated = true;
        this.loggedIn = response.data.user_id;
      }
    })
    .catch(error => {
        this.authenticated = false;
        console.log(error);
    });
  },*/
  //------- methods --------
  methods: {
    login() {
      if (this.input.username != "" && this.input.password != "") {
        axios
        .post(this.serviceURL+"/signin", {
            "username": this.input.username,
            "password": this.input.password
        }, {headers: {'Content-Type': 'application/json'}})
        .then(response => {
            if (response.data.status == "success") {
              this.authenticated = true;
              this.loggedIn = response.data.id;
            }
        })
        .catch(e => {
            alert("The username or password was incorrect, try again");
            this.input.password = "";
            console.log(e);
        });
      } else {
        alert("A username and password must be present");
      }
    },


    logout() {
      alert("No magic on the server yet. You'll have to write the logout code there.");
      axios
      .delete(this.serviceURL+"/signin")
      .then(response => {
          location.reload();
      })
      .catch(e => {
        console.log(e);
      });
    },


    fetchURLs() {
      axios
      .get(this.serviceURL+"/user/" + this.loggedIn + "/url")
      .then(response => {
        console.log(response.data);
          this.urlData = response.data;
      })
      .catch(e => {
        alert("Unable to load the url data");
        console.log(e);
      });
    },
    //TODO
    deleteURL(urlId) {
      axios
      .delete(this.serviceURL+"/url", {
        "url": urlId,  
        "username": this.loggedIn
      }, {headers: {'Content-Type': 'application/json'}})
      .then(response => {
          if (response.data.status == "success") {
            alert("The URL was deleted successfully");
          }
      })
      .catch(e => {
          alert("The URL was not deleted successfully");
          this.input.password = "";
          console.log(e);
      });
    },

    addUrl(){
      if (this.input.addUrl != "") {
        axios
        .post(this.serviceURL+"/url", {
            "username": this.input.username,
            "url": this.input.addUrlData
        }, {headers: {'Content-Type': 'application/json'}})
        .then(response => {
            if (response.data.status == "success") {
              this.authenticated = true;
              this.loggedIn = response.data.id;
            }
        })
        .catch(e => {
            alert("The URL was not added successfully");
            this.input.password = "";
            console.log(e);
        });
      } else {
        alert("please do not leave blank");
      }
    },

    selectSchool(schoolId) {
    	this.showModal();
      for (x in this.schoolsData) {
        if (this.schoolsData[x].schoolId == schoolId) {
          this.selectedSchool = this.schoolsData[x];
        }
      }
    },


    updateSchool(updatedSchool) {
      alert("This feature not available until YOUR version of schools.")
      // TODO: use axios.update to send the updated record to the service
    },

    showModal() {
      this.editModal = true;
    },


    hideModal() {
      this.editModal = false;
    }

  }
  //------- END methods --------

});
