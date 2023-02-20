VEHICLE_TYPE = (
    ('NON', 'Select Vehicle'),
    ('CAR', 'Car'),
    ('VAN', 'Van'),
    ('BIKE', 'Bike'),
    ('SUV', 'Suv'),
    ('TRUCK', 'Truck'),
    ('LONG', 'Long Vehicle')
)

BOOKING_STATUS = (
    ('PENDING', 'PENDING'),
    ('APPROVED', 'APPROVED'),
    ('CANCELED', 'CANCELED'),
)

SERVICE_STATUS = (
    ('PENDING', 'PENDING'),
    ('QUEUED', 'QUEUED'),
    ('ONGOING', 'ONGOING'),
    ('OVER', 'OVER'),
)

PAYMENT_STATUS = (
    ('PAYMENT_PENDING', 'PAYMENT_PENDING'),
    ('PAYMENT_PROCESSING', 'PAYMENT_PROCESSING'),
    ('PAYMENT_COMPLETED', 'PAYMENT_COMPLETED'),
    ('PAYMENT_NOT_VERIFIED', 'PAYMENT_NOT_VERIFIED'),
    ('PAYMENT_RESUBMISSION_REQUIRED', 'PAYMENT_RESUBMISSION_REQUIRED'),
)

DISTRICTS = (
    ('SelectDistrict', 'Select District'),
    ('Colombo', 'Colombo'),
)

DISTRICTS_CITY = (
    ('SelectCity', 'Select City'),
    ('Colombo 01', 'Colombo 01'),
    ('Colombo 02', 'Colombo 02'),
    ('Colombo 03', 'Colombo 03'),
    ('Colombo 04', 'Colombo 04'),
    ('Colombo 05', 'Colombo 05'),
    ('Colombo 06', 'Colombo 06'),
    ('Colombo 07', 'Colombo 07'),
    ('Colombo 08', 'Colombo 08'),
    ('Colombo 09', 'Colombo 09'),
    ('Colombo 10', 'Colombo 10'),
    ('Colombo 11', 'Colombo 11'),
    ('Colombo 12', 'Colombo 12'),
    ('Colombo 13', 'Colombo 13'),
    ('Colombo 14', 'Colombo 14'),
    ('Colombo 15', 'Colombo 15'),
    ('Dehiwala', 'Dehiwala'),
    ('Homagama', 'Homagama'),
    ('Kaduwela', 'Kaduwela'),
    ('Kesbewa', 'Kesbewa'),
    ('Kolonnawa', 'Kolonnawa'),
    ('Kotte', 'Kotte'),
    ('Maharagama', 'Maharagama'),
    ('Moratuwa', 'Moratuwa'),
    ('Padukka', 'Padukka'),
    ('Ratmalana', 'Ratmalana'),
    ('Seethawaka', 'Seethawaka'),
    ('Thimbirigasyaya', 'Thimbirigasyaya'),

)


ALL_DISTRICT = (
    ('Gampaha', 'Gampaha'),
    ('Kalutara', 'Kalutara'),
    ('Kandy', 'Kandy'),
    ('Matale', 'Matale'),
    ('NuwaraEliya', 'NuwaraEliya'),
    ('Galle', 'Galle'),
    ('Matara', 'Matara'),
    ('Hambantota', 'Hambantota'),
    ('Jaffna', 'Jaffna'),
    ('Kilinochchi', 'Kilinochchi'),
    ('Mannar', 'Mannar'),
    ('Vavuniya', 'Vavuniya'),
    ('Mullaitivu', 'Mullaitivu'),
    ('Batticaloa', 'Batticaloa'),
    ('Ampara', 'Ampara'),
    ('Trincomalee', 'Trincomalee'),
    ('Kurunegala', 'Kurunegala'),
    ('Puttalam', 'Puttalam'),
    ('Anuradhapura', 'Anuradhapura'),
    ('Polonnaruwa', 'Polonnaruwa'),
    ('Badulla', 'Badulla'),
    ('Moneragala', 'Moneragala'),
    ('Ratnapura', 'Ratnapura'),
    ('Kegalle', 'Kegalle'),
)

SHOP_REPORT_TYPES = (
    ('ALL_SERVICES', 'ALL_SERVICES'),
    ('ALL_PAYMENTS', 'ALL_PAYMENTS')
)

USER_REPORT_TYPES = (
    ('BOOKED_SERVICES', 'BOOKED_SERVICES'),
    ('CONFIRMED_SERVICES', 'CONFIRMED_SERVICES')
)

PAYMENT_DEFAULT_SLIP = "/media/users/payment/payment_not_submitted.jpg"
