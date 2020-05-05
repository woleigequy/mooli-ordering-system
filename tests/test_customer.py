import models.model_customer as m
import controllers.controller_customer as c

print('[UNIT TESTING] Testing: Customer...')

m.add_customer('Bowen_WU', 'bowenwu@gmail.com', 'Testpassword12', 'Bowen', 'WU', 'M', '(310)-873-7333')
m.verify_credential('Bowen_WU', 'Testpassword12 ')
m.change_password('1000000', 'Testpassword123')
m.verify_credential('Bowen_WU', 'Testpassword123')
assert c.sign_up('RyanLam', 'ryan@gmail.com', 'Testpassword12345', 'Ryan', 'Lam', 'M') == {'message': 'You account has been created successfully.'}
m.verify_credential('RyanLam', 'Testpassword12345 ')
assert c.update_customer_info(1000001, 'Ryan', 'Wong', 'F', '911') == {'message': 'You account info has been updated successfully.'}
assert c.change_password('1000001', 'Testpassword12345', 'Testpassword123', 'Testpassword123') == {'message': 'You password has been updated successfully.'}
m.verify_credential('RyanLam', 'Testpassword123')
# When original password is wrong
assert c.change_password('1000001', 'Testpassword12345', 'Testpassword123', 'Testpassword123') == {'error': 'Invalid password'}
# When the new password and verify password don't match
c.change_password('1000001', 'Testpassword123', 'Testpassword1234', 'Testpassword123') == {'error': 'Passwords do not match.'}


print('[UNIT TESTING] Customer has passed all the tests')
