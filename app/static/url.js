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
              this.fetchURLs();
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
        if (response.data.length == 0) {
          alert("User has no URLs saved")
        }
        this.urlData = response.data;
      })
      .catch(e => {
        alert("Unable to load the url data");
        console.log(e);
      });
    },
    deleteURL(urlId) {
      axios
      .delete(this.serviceURL+"/url", {
        data: {
          "url": urlId,  
          "username": this.loggedIn
        }
      }, {headers: {'Content-Type': 'application/json'}}) 
      .then(response => {
          console.log(response)
          if (response.data.status == 200) {
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
      if (validate(this.input.addUrlData)) {
        axios
        .post(this.serviceURL+"/url", {
            "username": this.input.username,
            "url": this.input.addUrlData
        }, {headers: {'Content-Type': 'application/json'}})
        .then(response => {
            if (response.data.status == "success") {
              this.authenticated = true;
              this.loggedIn = response.data.id;
              this.fetchURLs();
            }
        })
        .catch(e => {
            alert("The URL was not added successfully");
            this.input.password = "";
            console.log(e);
        });
      } else {
        alert("This URL is invalid");
      }
    },

    addAndFetchURLs(){
      this.addUrl();
      this.fetchURLs();
    },

    copy(tinyURL){
      copyUrl = "https://cs3103.cs.unb.ca:8028/" + tinyURL
      navigator.clipboard.writeText(copyUrl)
    }
  }
  //------- END methods --------

});

function validate(url){
  try{
    new URL(url)
    return true;
  }
  catch(e){
    return false;
  }
}