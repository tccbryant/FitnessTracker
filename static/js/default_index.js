// This is the js for the default/index.html view.
/*
set_self >> 
get_my_plans
get_followed_plans
get_all_plans
get_5_plans
get_20_plans


get_profile
edit_plan (called when plans are open).
delete_plan (called when open or closed.)
archive_plan
add_plan (called when no plans are open.)
follow_plan (add plan id to db)
set_plan_as_current
get_current (calls open plan on current.)
open_plan


add_day (adds a day into the plan schedule.)
edit_day
save_plan (edit the db and exit, call get_my_plan.)
cancel_plan (exit)

data:
my_plans = []
followed_plans = []
all_plans = []
self_id = []

plan_days = []

*/
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

    self.log_in = function() {
        $.getJSON(log_in_url,
            function(data) {
                if (data.logged_in) {
                    self.vue.page = 'profile';
                    self.get_profile();
                    self.get_my_plans();
                }
            }
        );
    }
    
    self.get_profile = function() {
        $.getJSON(get_profile_url,
            function(data) {
                self.vue.user_profile = data.profile;
                self.vue.profile_loaded = true;
                /*  Dict containing the Height,
                 *  Weight, Goals, of user,
                 *  as well as the current plan
                 *  that the user is undergoing.
                 * 
                 *  Convert active plan to id in
                 *  the api for this function.
                 */
            }
        );
    };
    
    self.edit_profile = function() {
        console.log(self.vue.user_profile);
        $.post(edit_profile_url,
            {
                height: self.vue.user_profile.height,
                weight: self.vue.user_profile.weight
                // Send changed values within user_profile dict
                // to the DB. 

                // In HTML, make an edit button. If editting, show
                // a button that calls this function and another
                //"cancel button" that calls "get_profile";
            }
        );
    };


    self.adding_plan = function() {
        self.vue.page = 'adding';
    };

    self.profile = function() {
        self.vue.page = 'profile';
    };

    self.viewing = function() {
        self.vue.page = 'viewing';
    };

    self.add_plan = function() {

        var title = $('input#title_input').val();
        var goals = $('input#goals_input').val();
        var results = $('input#results_input').val();
        var feedback = $('input#feedback_input').val();

        $.post(add_plan_url,
            {
                title: title,
                goals: goals,
                results: results,
                feedback: feedback
            },
            function(data) {
                console.log(data);
            }
        );
        self.profile();
        self.get_my_plans();
    };

    self.get_my_plans = function() {
        $.getJSON(get_my_plans_url,
            function(data) {
                self.vue.my_plans=data.my_plans;
                console.log(self.vue.my_plans);
            }
        );

    };

    self.delete_plan = function(plan_id) {
        $.post(delete_plan_url,
            {
                plan_id: plan_id
            },
            function() {
                self.get_my_plans();
            }
        )
    };

    self.view_plan = function(plan_id) {
        $.getJSON(view_plan_url,
            {
                plan_id: plan_id
            },
            function(data) {
                self.vue.open_plan = data.plan;
                self.viewing();
            }
        )
    };

    self.browse = function() {
        $.getJSON(browse_url,
            function(data) {
                self.vue.browse_plans = data.plans;
            }
        )
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            //plan_is_open: false,
            page: 'default',
            user_profile: null,
            open_plan: null,
            my_plans: [], /* dict with texts and archive bool for now. */
            followed_plans: [],
            browse_plans: [],
            profile_loaded: false,
            

        },
        methods: {
            get_profile: self.get_profile,
            edit_profile: self.edit_profile,
            add_plan: self.add_plan,
            adding_plan: self.adding_plan,
            profile: self.profile,
            get_my_plans: self.get_my_plans,
            log_in: self.log_in,
            delete_plans: self.delete_plan,
            view_plan: self.view_plan,
            viewing: self.viewing,
            browse: self.browse
        }

    });
    self.log_in();

    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});

