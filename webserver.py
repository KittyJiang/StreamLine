############################### RUNS THE SITE ###############################

# NOTE: KEEP THIS SCRIPT CLEAN AND BASICALLY IMPORT ALL METHODS FROM OTHER PYTHON FILES WE WRITE

############# IMPORTS#############
# LIBRARIES
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine

# FILES
import db_connect as db

import landing
import login
import signup

import profile_recom as pr
import profile_edit as prof_edit
import profile_history as prof_hist

############# GLOBAL VARIABLES #############
# CONNECT TO DATABASE

############# METHODS #############

############# PAGES #############
app = Flask(__name__)

# landing page
@app.route('/')
def home():
    page = landing.bootstrap_landing()
    return page
# above is format for all methods below:
    # actual render_template all done in main methods of individual py scripts
    # that is returned up to this central file


# sign up page
@app.route('/signup')
def sign_up():
    page = signup.main()
    return render_template('bootstrap-login-signup.html')

# sign up succeed page
@app.route('/signup/success')
def sign_up_success():
    page = signup.success()
    return page

# import watchlist - sign up version
@app.route('/signup/watchimport')
def sign_up_watchImport():
    page = "Sign Up through Importing list"
    return page


# log in page
@app.route('/login')
def login():
    page = "Login Page"
    return render_template('bootstrap-login-login.html')



# movie/show search page
@app.route('/browse')
def browse():
    page = "Browse catalog page"
    return page

# movie/show profile page

##############################################################
# PROFILE SEGMENT

# NOTE: IF CREATE PUBLIC PROFILE KIND OF THING, CHANGE BELOW "PROFILE" ALL INTO "SETTINGS"
    # SET LOGIN VERIFICATION TO SEPARATE PUBLIC AND PRIVATE CODE

# # PROFILE BLUEPRINT
# import profile
# app.register_blueprint(profile.bp)

################# EDIT #################
# user profile main page; auto routes to edit profile page
@app.route('/profile')
@app.route('/profile/edit')
def profile_edit():
    # need to make this variable through login verification
    username = "PROTOTYPE_TEST"

    # get user bio
    bio = prof_edit.get_bio(username)

    # get user top three genre
    top_three = prof_edit.three_genre(prof_edit.ranked_genre(username))
    # print(top_three)

    # need to be able to edit author cards later
    profile = {'username':username,
                'bio': bio,
                'top_three':top_three}

    # page = prof_edit.main('profile/profile-edit.html', username)
    # return page
    return render_template('profile/profile-edit.html', profile=profile)

@app.route('/profile/edit-bio', methods=('GET', 'POST'))
def profile_edit_bio():
    # come back and find way to pass this variable later, maybe /profile/edit-bio/<username>
    username = "PROTOTYPE_TEST"

    bio = prof_edit.get_bio(username)

    if request.method == 'POST':
        bio_body = request.form['bio_body']
        prof_edit.update_sql_bio(username, bio_body)
        return redirect(url_for('profile_edit'))

    profile = {'username':username,
                'bio': bio}
    return render_template('profile/profile-edit-bio.html', profile=profile)

################# HISTORY #################
# user profile history and watchlist page
@app.route('/profile/history')
def profile_history():
    # list of watchlist tables and files
    watchlists = []
    # TESTING HARDCODE, GET RID OF LATER; dictionary in list
    watchlists.append({'title':'My Watchlist', 'file':'IMDb_Watchlist_Jenny'})

    # list of recent videos; restrict to 4 titles
    recents = []
    # TESTING HARDCODE DUMMY
    recents.extend(['Reservoir Dogs', 'Moonlight', 'Westworld', 'Luke Cage'])

    # dictionary containing page content
    page = {'watchlists': watchlists,
            'recents': recents }
    return render_template('profile/profile-history.html', page=page)

# page from user profile specifically to a watchlist
@app.route('/profile/watchlist/<watch_name>', methods=('GET', 'POST'))
def profile_watchlist_each(watch_name):
    # watchlist name
    # watchlist = {}
    # TESTING HARDCODE, TAKE CARE IN SQL AND GET RID LATER
    watchlist = prof_hist.parse_watchlist_for_page("IMDb_Watchlist_Jenny", "Parsed_Watchlist_Jenny")

    return render_template('/profile/profile-watchlist-each.html', watch_name=watch_name, watchlist=watchlist)

# user adding watchlist
@app.route('/profile/watchlist/add', methods=('GET','POST'))
def profile_watchlist_add():
    return render_template('/profile/profile-watchlist-add.html')

################# RECOMMENDATION #################
# streaming service recommendation
@app.route('/profile/recommendation')
def profile_recommendation():
#     page = "Profile recommendation page"
    page = pr.main('profile/profile-recommendation.html','Parsed_Watchlist_Jenny')
    return page

################# SECURITY #################
# user profile security and login page
@app.route('/profile/security')
def profile_security():
#    page = "Profile security page"
    return render_template('profile/profile-security.html')

################# LINKED #################
# user profile linked accounts page
@app.route('/profile/linked')
def profile_linked():
    # get boolean statuses from sql
    # eventually route directly to account page

    # TESTING HARDCODE WHILE MYSQL IS DOING SOMETHING WEIRD
#    page = "Profile linked page"
    return render_template('profile/profile-linked.html')

################# PREFERENCES #################
# user profile content preferences page
@app.route('/profile/preferences')
def profile_preferences():
#    page = "Profile preferences page"
    return render_template('profile/profile-preference.html')

# import watchlist - user profile version
# INCOMPLETE TEMPLATE
@app.route('/profile/import')
def profile_import():
#    page = "Profile import page"
    return render_template('profile/profile-generic.html')

# watchlist pages
# INCOMPLETE TEMPLATE
@app.route('/watchlist')
def profile_watchlist():
    # will have arguments in url for each unique watchlist
#    page = "Profile watchlist page"
    return render_template('profile/profile-generic.html')

# refining user preference page
# INCOMPLETE TEMPLATE
@app.route('/recommendation/refine')
def profile_recommendation_refine():
    page = "Profile recommentation refine page"
    return page

# results page


##############################################################
# OPTIONAL TEST PAGES
# TESTING FOOTER
@app.route('/test')
def test_page():
    return render_template('header-footer.html')

@app.route('/test/bootstrap')
def test_bootstrap():
    return render_template('bootstrap_template.html')

@app.route('/test/justwatch')
def test_justwatch():
    return render_template('test-justwatch.html')

@app.route('/test/profile-gen-kitty')
def test_profile_gen_kitty():
    return render_template('profile/profile-generic.html')

# about us page
@app.route('/about')
def about():
    page_content = ['This is the about page.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultricies ullamcorper ante et placerat. Integer ut diam nec ipsum condimentum aliquet ut ac leo. Sed pretium velit nisi, sed pulvinar ante porta vel. Suspendisse et posuere ex. Etiam tincidunt tempor turpis, quis lacinia tellus ultricies ac. Nam rutrum orci nulla, vitae dictum nulla vulputate a. Morbi libero sapien, sollicitudin eu nisi id, posuere porta urna. Morbi gravida elit nisl, eu gravida arcu pretium id. Vivamus magna mi, fermentum in placerat vel, tincidunt tincidunt purus.', 'Integer condimentum magna mattis nisi condimentum, sollicitudin luctus ligula elementum. Sed rhoncus ante quis sollicitudin dictum. Pellentesque finibus lectus quis nibh ullamcorper aliquam. Cras sed aliquet sapien. Vivamus blandit tempor turpis nec condimentum. Phasellus ornare id dui a tincidunt. Morbi congue mi quis tempor cursus. In ac suscipit dui, id efficitur turpis. Phasellus varius leo eget dolor pellentesque consequat. Nam eu libero nisl. Sed consectetur ante elit, in commodo diam interdum quis. Aenean feugiat porta est vitae condimentum. Cras ornare ante tellus, sed mattis ligula egestas tempus. Donec sodales tellus mi, non ultricies diam auctor et. Quisque congue venenatis mauris, non convallis felis sodales a.', 'Donec aliquet lectus vitae mi consequat, vitae rutrum orci tempus. Suspendisse at erat quis nisl elementum molestie. Proin aliquet gravida posuere. Aenean vitae lobortis ipsum. Integer blandit massa enim. Donec consectetur tellus ut lorem venenatis gravida ac eu velit. Etiam auctor mauris nulla, sit amet euismod libero eleifend at. Ut risus est, elementum vitae augue dapibus, laoreet convallis sem. Vestibulum eget erat sapien. Curabitur non placerat libero, eu feugiat nisl.']
    return render_template('one-column-footer-page.html', title="About Us", page_content=page_content)

# contact us page
@app.route('/contact')
def contact():
    page_content = ['This is the contact page.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultricies ullamcorper ante et placerat. Integer ut diam nec ipsum condimentum aliquet ut ac leo. Sed pretium velit nisi, sed pulvinar ante porta vel. Suspendisse et posuere ex. Etiam tincidunt tempor turpis, quis lacinia tellus ultricies ac. Nam rutrum orci nulla, vitae dictum nulla vulputate a. Morbi libero sapien, sollicitudin eu nisi id, posuere porta urna. Morbi gravida elit nisl, eu gravida arcu pretium id. Vivamus magna mi, fermentum in placerat vel, tincidunt tincidunt purus.', 'Integer condimentum magna mattis nisi condimentum, sollicitudin luctus ligula elementum. Sed rhoncus ante quis sollicitudin dictum. Pellentesque finibus lectus quis nibh ullamcorper aliquam. Cras sed aliquet sapien. Vivamus blandit tempor turpis nec condimentum. Phasellus ornare id dui a tincidunt. Morbi congue mi quis tempor cursus. In ac suscipit dui, id efficitur turpis. Phasellus varius leo eget dolor pellentesque consequat. Nam eu libero nisl. Sed consectetur ante elit, in commodo diam interdum quis. Aenean feugiat porta est vitae condimentum. Cras ornare ante tellus, sed mattis ligula egestas tempus. Donec sodales tellus mi, non ultricies diam auctor et. Quisque congue venenatis mauris, non convallis felis sodales a.', 'Donec aliquet lectus vitae mi consequat, vitae rutrum orci tempus. Suspendisse at erat quis nisl elementum molestie. Proin aliquet gravida posuere. Aenean vitae lobortis ipsum. Integer blandit massa enim. Donec consectetur tellus ut lorem venenatis gravida ac eu velit. Etiam auctor mauris nulla, sit amet euismod libero eleifend at. Ut risus est, elementum vitae augue dapibus, laoreet convallis sem. Vestibulum eget erat sapien. Curabitur non placerat libero, eu feugiat nisl.']
    return render_template('one-column-footer-page.html', title="Contact Us", page_content=page_content)

# privacy policy page
@app.route('/privacy')
def privacy():
    page_content = ['This is the privacy page.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultricies ullamcorper ante et placerat. Integer ut diam nec ipsum condimentum aliquet ut ac leo. Sed pretium velit nisi, sed pulvinar ante porta vel. Suspendisse et posuere ex. Etiam tincidunt tempor turpis, quis lacinia tellus ultricies ac. Nam rutrum orci nulla, vitae dictum nulla vulputate a. Morbi libero sapien, sollicitudin eu nisi id, posuere porta urna. Morbi gravida elit nisl, eu gravida arcu pretium id. Vivamus magna mi, fermentum in placerat vel, tincidunt tincidunt purus.', 'Integer condimentum magna mattis nisi condimentum, sollicitudin luctus ligula elementum. Sed rhoncus ante quis sollicitudin dictum. Pellentesque finibus lectus quis nibh ullamcorper aliquam. Cras sed aliquet sapien. Vivamus blandit tempor turpis nec condimentum. Phasellus ornare id dui a tincidunt. Morbi congue mi quis tempor cursus. In ac suscipit dui, id efficitur turpis. Phasellus varius leo eget dolor pellentesque consequat. Nam eu libero nisl. Sed consectetur ante elit, in commodo diam interdum quis. Aenean feugiat porta est vitae condimentum. Cras ornare ante tellus, sed mattis ligula egestas tempus. Donec sodales tellus mi, non ultricies diam auctor et. Quisque congue venenatis mauris, non convallis felis sodales a.', 'Donec aliquet lectus vitae mi consequat, vitae rutrum orci tempus. Suspendisse at erat quis nisl elementum molestie. Proin aliquet gravida posuere. Aenean vitae lobortis ipsum. Integer blandit massa enim. Donec consectetur tellus ut lorem venenatis gravida ac eu velit. Etiam auctor mauris nulla, sit amet euismod libero eleifend at. Ut risus est, elementum vitae augue dapibus, laoreet convallis sem. Vestibulum eget erat sapien. Curabitur non placerat libero, eu feugiat nisl.']
    return render_template('one-column-footer-page.html', title="Privacy Policy", page_content=page_content)

# FAQ page
@app.route('/faq')
def faq():
    page_content = ['This is the faq page.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultricies ullamcorper ante et placerat. Integer ut diam nec ipsum condimentum aliquet ut ac leo. Sed pretium velit nisi, sed pulvinar ante porta vel. Suspendisse et posuere ex. Etiam tincidunt tempor turpis, quis lacinia tellus ultricies ac. Nam rutrum orci nulla, vitae dictum nulla vulputate a. Morbi libero sapien, sollicitudin eu nisi id, posuere porta urna. Morbi gravida elit nisl, eu gravida arcu pretium id. Vivamus magna mi, fermentum in placerat vel, tincidunt tincidunt purus.', 'Integer condimentum magna mattis nisi condimentum, sollicitudin luctus ligula elementum. Sed rhoncus ante quis sollicitudin dictum. Pellentesque finibus lectus quis nibh ullamcorper aliquam. Cras sed aliquet sapien. Vivamus blandit tempor turpis nec condimentum. Phasellus ornare id dui a tincidunt. Morbi congue mi quis tempor cursus. In ac suscipit dui, id efficitur turpis. Phasellus varius leo eget dolor pellentesque consequat. Nam eu libero nisl. Sed consectetur ante elit, in commodo diam interdum quis. Aenean feugiat porta est vitae condimentum. Cras ornare ante tellus, sed mattis ligula egestas tempus. Donec sodales tellus mi, non ultricies diam auctor et. Quisque congue venenatis mauris, non convallis felis sodales a.', 'Donec aliquet lectus vitae mi consequat, vitae rutrum orci tempus. Suspendisse at erat quis nisl elementum molestie. Proin aliquet gravida posuere. Aenean vitae lobortis ipsum. Integer blandit massa enim. Donec consectetur tellus ut lorem venenatis gravida ac eu velit. Etiam auctor mauris nulla, sit amet euismod libero eleifend at. Ut risus est, elementum vitae augue dapibus, laoreet convallis sem. Vestibulum eget erat sapien. Curabitur non placerat libero, eu feugiat nisl.']
    return render_template('one-column-footer-page.html', title="FAQ", page_content=page_content)

# Requires different template from above
# sitemap page
@app.route('/sitemap')
def sitemap():
    page = "Sitemap page"
    return page

# Requires different template form above
# Report bugs page
@app.route('/bugs')
def bugs():
    page = "Report bugs page"
    return page


###############################
app.run(host='0.0.0.0', port=5000, debug=True)
# app.run(host='35.245.57.180', port=5000, debug=True)