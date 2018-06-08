// This is the js for the default/index.html view.

set_self >> 
get_my_plans
get_followed_plans
get_all_plans
get_5_plans
get_20_plans
edit_plan (called when plans are open).
delete_plan (called when open or closed.)
add_plan (called when no plans are open.)
follow_plan (add plan id to db)
set_plan_as_current
archive_plan
get_current (calls open plan on current.)
open_plan
add_day (adds a day into the plan schedule.)
save_plan (edit the db and exit, call get_my_plan.)
cancel_plan (exit)

data:
my_plans = []
followed_plans = []
all_plans = []
self_id = []
plan_days = []

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    // Enumerates an array.
    var enumerate = function(v) { var k=0; return v.map(function(e) {e._idx = k++;});};

    self.open_uploader = function () {
        $("div#uploader_div").show();
        self.vue.is_uploading = true;
    };

    self.close_uploader = function () {
        $("div#uploader_div").hide();
        self.vue.is_uploading = false;
        $("input#file_input").val(""); // This clears the file choice once uploaded.

    };

    self.upload_file = function (event) {
        // Reads the file.
        var input = event.target;
        var file = document.getElementById("file_input");//input.files[0];
        if (file) {
            // First, gets an upload URL.
            console.log("Trying to get the upload url");
            $.getJSON('https://upload-dot-luca-teaching.appspot.com/start/uploader/get_upload_url',
                function (data) {
                    // We now have upload (and download) URLs.
                    var put_url = data['signed_url'];
                    var get_url = data['access_url'];
                    console.log("Received upload url: " + put_url);
                    // Uploads the file, using the low-level interface.
                    var req = new XMLHttpRequest();
                    req.addEventListener("load", self.upload_complete(get_url));
                    // TODO: if you like, add a listener for "error" to detect failure.
                    req.open("PUT", put_url, true);
                    req.send(file);
                });
        }
    };


    self.upload_complete = function(get_url) {
        // Hides the uploader div.
        self.close_uploader();
        console.log('The file was uploaded; it is now available at ' + get_url);
        //TODO: The file is uploaded.  Now you have to insert the get_url into the database, etc.
        $.post(add_image_url,
            {
                image_url: get_url,
                image_price: self.vue.image_price
            },
            function(){
                console.log(self.vue.image_price)
                setTimeout(function() {
                    self.get_images();
                }, 200);
            }
        )
    };

    self.get_images = function() {
        if(self.vue.user_id == null) {
            self.vue.user_id = self.vue.self_id;
        }
        $.getJSON(images_url,
            {
                user_id: self.vue.user_id
            },
            function(data) {
                self.vue.user_images = data.user_images;
            }
        )
    };

    self.get_users = function() {
        $.getJSON(users_url,
            function(data) {
                self.vue.users = data.users;
                console.log(self.vue.users)
            }
        );
    };

    self.set_user = function(user_id) {
        self.vue.user_id = user_id;
        self.vue.self_page = user_id==self.vue.self_id;
        self.get_images();
    };

    self.set_self = function() {
        $.getJSON(self_url,
            function(data) {
                self.vue.self_id = data.id;
                self.vue.self_page = data.id >= 0;
            }
        );
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            user_images: [],
            users: [],
            is_uploading: false,
            self_page: true, // Leave it to true, so initially you are looking at your own images.
            user_id: null, //should be set to self id
            self_id: null,
            image_price: null
        },
        methods: {
            open_uploader: self.open_uploader,
            close_uploader: self.close_uploader,
            upload_file: self.upload_file,
            get_images: self.get_images,
            get_users: self.get_users,
            set_user: self.set_user,
            set_self: self.set_self
        }

    });

    self.set_self();
    self.get_users();
    setTimeout(function() {
        self.get_images();
    }, 100);
    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});

