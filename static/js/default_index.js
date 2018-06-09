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
    };

    
    self.edit_plan = function(plan_id) {
        //HTML, call on edit_plan(my_plans[._idx].id), something like this.
        self.vue.is_editing_plan = true; //open new page with plan editing.
    }

    self.save_plan = function(plan_id) {
        self.vue.is_editing_plan = false;
        self.vue.is_adding_plan = false;
    }

    /*
    self.delete_plan = function(){

    }

    self.plan_arch_toggle = function(){

    }

    self.set_plan_current = function(){

    }

    self.get_current_plan = function() {
        self.vue.open_plan_id = self.vue.user_profile.active_plan;
        self.show_plan();
    }

    self.show_plan = function() {
        $.getJSON(show_plan_url,
            {
                plan_id: self.vue.open_plan_id
            },
            function(data) {
                self.vue.open_plan_obj = data.plan;
                self.vue.plan_is_open = true;
            }
        )
    }

    self.get_my_plans = function() {
        $.getJSON(get_my_plans_url,
            function(data) {
                self.vue.my_plans = data.user_plans
                //Array of Dict of plan descriptions 
                //for populating profile page.
            }
        );
    }

    self.get_followed_plans = function() {
        $.getJSON(get_followed_plans_url,
            function(data) {
                self.vue.followed_plans = data.followed_plans
            }
        );
    }


    */

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            //plan_is_open: false,
            page: 'profile',
            user_profile: null,
            open_plan: null,
            cur_edit: null, //array of size 1.
            my_plans: [], /* dict with texts and archive bool for now. */
            followed_plans: [],
            profile_loaded: false,
            

        },
        methods: {
            get_profile: self.get_profile,
            edit_profile: self.edit_profile,
            add_plan: self.add_plan,
            edit_plan: self.edit_plan,
            adding_plan: self.adding_plan,
            profile: self.profile
        }

    });

    self.get_profile();
    
    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});

