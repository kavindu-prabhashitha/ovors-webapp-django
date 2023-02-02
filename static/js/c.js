var state_arr = new Array(
    'Colombo', 'Gampaha', 'Kalutara', 'Kandy', 'Matale',
    'Nuwara Eliya', 'Galle', 'Matara', 'Hambantota', 'Jaffna',
    'Kilinochchi', 'Mannar', 'Vavuniya', 'Mullaitivu', 'Batticaloa',
    'Ampara', 'Trincomalee', 'Kurunegala', 'Puttalam', 'Anuradhapura',
    'Polonnaruwa', 'Badulla', 'Moneragala', 'Ratnapura', 'Kegalle'
)

var s_a = new Array();

s_a[0] = "";
s_a[1] = "Colombo 01 | Colombo 02 | Colombo 03 | Colombo 04 | Colombo 05 | Colombo 06 | Colombo 07 | Colombo 08 | Colombo 09 | Colombo 10 | Colombo 11 | Colombo 12 | Colombo 13 | Dehiwala | Homagama  | Kaduwela | Kesbewa | Kolonnawa  | Kotte | Maharagama | Moratuwa | Padukka | Ratmalana | Seethawaka | Thimbirigasyaya";
s_a[2] = "Attanagalla | Biyagama | Divulapitiya | Dompe | Gampaha | Ja-Ela | Katana | Kelaniya | Mahara | Minuwangoda | Mirigama | Negombo | Wattala";
s_a[3] = "Agalawatta | Bandaragama | Beruwala | Bulathsinhala | Dodangoda | Horana | Ingiriya | Kalutara | Madurawela | Mathugama | Millaniya | Palindanuwara | Panadura | Walallavita";
s_a[4] = "Akurana | Delthota | Doluwa | Gagawata Korale | Ganga Ihala Korale | Harispattuwa | Hatharaliyadda | Kundasale | Medadumbara | Minipe | Panvila | Pasbage Korale | Pathadumbara | Pathahewaheta | Poojapitiya | Thumpane | Udadumbara | Udapalatha | Udunuwara | Yatinuwara";
s_a[5] = "Galewela | Matale | Yatawatta | Wilgamuwa | Rathtota | Rathtota | Ambangaga Korale | Dambulla | Pallepola | Ukuwela | Naula | Laggala - Pallegama";
s_a[6] = "town31 | town32 | town33 | town34 | town35 | town36";
s_a[7] = "town37 | town38 | town39 | town40 | town41 | town42";
s_a[8] = "town43 | town44 | town45 | town46 | town47 | town48";

function print_state(state_id){
    var option_str = document.getElementById(state_id);
    option_str.length=0;
    option_str.options[0] = new Option('Select State District', '');
    option_str.selectedIndex = 0;
    for(var i=0; i<state_arr.length; i++){
        option_str.options[option_str.length] = new Option(state_arr[i], state_arr[i]);
    }
}

function print_city(city_id, city_index){
    var option_str = document.getElementById(city_id);
    option_str.length = 0;
    option_str.options[0] = new Option('Select City', '');
    option_str.selectedIndex = 0;
    var city_arr = s_a[city_index].split("|");
    for(var i=0; i<city_arr.length; i++){
        option_str.options[option_str.length] = new Option(city_arr[i], city_arr[i]);
    }
}