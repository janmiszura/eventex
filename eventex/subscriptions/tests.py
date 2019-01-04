from django.test import TestCase
from django.core import mail
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')
    
    def test_get(self):
        """get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)
    
    def test_template(self):
        """must use template subscriptions/subscrition_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')
    
    def test_html(self):
        """must contais input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, 'input type', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')
    
    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Jan Miszura', cpf='12345678901', 
                email='janmiszura@gmail.com', phone='62999999999')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid post should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)
    
    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))
    
    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expected = 'Confirmação de Inscrição'
        self.assertEqual(expected, email.subject)
    
    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expected = 'contato@eventex.com.br'
        self.assertEqual(expected, email.from_email)
    
    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expected = ['contato@eventex.com.br', 'janmiszura@gmail.com']
        self.assertEqual(expected, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]
        self.assertIn('Jan Miszura', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('janmiszura@gmail.com', email.body)
        self.assertIn('62999999999', email.body)
