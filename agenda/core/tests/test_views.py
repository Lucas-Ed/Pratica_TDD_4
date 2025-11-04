from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Agenda


class AgendaViewsTestCase(TestCase):

    def setUp(self):
        # Cria um usuário para autenticação
        self.user = User.objects.create_user(username='testeuser', email='teste@fatec.sp.gov.br', password='123456')
        self.client = Client()
        self.client.login(username='testeuser', password='123456')

        # Cria um contato para os testes de edição e exclusão
        self.contato = Agenda.objects.create(
            nome_completo="Contato de Teste",
            telefone="11999999999",
            email="teste@teste.com",
            observacao="Contato inicial para testes"
        )

    def test_index_page_requires_login(self):
        """Verifica se a página inicial exige login"""
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_index_page_logged_user(self):
        """Verifica se a página inicial carrega corretamente para usuários logados"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_listar_contatos(self):
        """Verifica se a listagem de contatos funciona"""
        response = self.client.get(reverse('listar_contatos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listar.html')
        self.assertContains(response, "Contato de Teste")

    def test_cadastrar_contato(self):
        """Testa o cadastro de um novo contato"""
        data = {
            'nome_completo': 'Novo Contato',
            'telefone': '11888888888',
            'email': 'novo@teste.com',
            'observacao': 'Criado via teste automatizado'
        }
        response = self.client.post(reverse('cadastrar_contato'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Agenda.objects.filter(nome_completo='Novo Contato').exists())

    def test_editar_contato(self):
        """Testa a atualização de um contato existente"""
        data = {
            'nome_completo': 'Contato Atualizado',
            'telefone': '11777777777',
            'email': 'atualizado@teste.com',
            'observacao': 'Alterado no teste'
        }
        response = self.client.post(reverse('editar_contato', args=[self.contato.id]), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.contato.refresh_from_db()
        self.assertEqual(self.contato.nome_completo, 'Contato Atualizado')

    def test_excluir_contato(self):
        """Testa a exclusão de um contato"""
        response = self.client.post(reverse('excluir_contato', args=[self.contato.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Agenda.objects.filter(id=self.contato.id).exists())

    def test_acesso_sem_login_redireciona(self):
        """Verifica se todas as rotas de CRUD redirecionam sem login"""
        self.client.logout()
        urls = [
            reverse('index'),
            reverse('listar_contatos'),
            reverse('cadastrar_contato'),
            reverse('editar_contato', args=[self.contato.id]),
            reverse('excluir_contato', args=[self.contato.id]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login/', response.url)