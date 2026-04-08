from __future__ import annotations

from decimal import Decimal

from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from data.repository import ImovelRepository


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.repo = ImovelRepository()

        self.setWindowTitle("Portal Imobiliário")
        self.resize(1200, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab_listar = QWidget()
        self.tab_pesquisar = QWidget()
        self.tab_criar = QWidget()

        self.tabs.addTab(self.tab_listar, "Listar")
        self.tabs.addTab(self.tab_pesquisar, "Pesquisar")
        self.tabs.addTab(self.tab_criar, "Criar anúncio")

        self._build_listar_tab()
        self._build_pesquisar_tab()
        self._build_criar_tab()

    def _build_listar_tab(self):
        layout = QVBoxLayout()

        self.btn_refresh = QPushButton("Atualizar lista")
        self.btn_refresh.clicked.connect(self._carregar_lista)

        self.tbl_listar = QTableWidget(0, 7)
        self.tbl_listar.setHorizontalHeaderLabels(
            ["ID", "Morada", "Preço", "Quartos", "WC", "Área", "Localização"]
        )

        layout.addWidget(self.btn_refresh)
        layout.addWidget(self.tbl_listar)
        self.tab_listar.setLayout(layout)

        self._carregar_lista()

    def _build_pesquisar_tab(self):
        root = QVBoxLayout()
        linha_texto = QHBoxLayout()
        linha_local = QHBoxLayout()

        self.search_text = QLineEdit()
        self.search_text.setPlaceholderText("morada ou descrição")
        self.search_preco_max = QLineEdit()
        self.search_preco_max.setPlaceholderText("preço máximo (opcional)")

        self.search_distrito = QComboBox()
        self.search_concelho = QComboBox()
        self.search_freguesia = QComboBox()

        self.search_distrito.currentIndexChanged.connect(self._on_distrito_changed)
        self.search_concelho.currentIndexChanged.connect(self._on_concelho_changed)

        btn_search = QPushButton("Pesquisar")
        btn_search.clicked.connect(self._pesquisar)

        linha_texto.addWidget(QLabel("Texto:"))
        linha_texto.addWidget(self.search_text)
        linha_texto.addWidget(QLabel("Preço máx:"))
        linha_texto.addWidget(self.search_preco_max)

        linha_local.addWidget(QLabel("Distrito:"))
        linha_local.addWidget(self.search_distrito)
        linha_local.addWidget(QLabel("Concelho:"))
        linha_local.addWidget(self.search_concelho)
        linha_local.addWidget(QLabel("Freguesia:"))
        linha_local.addWidget(self.search_freguesia)
        linha_local.addWidget(btn_search)

        self.tbl_search = QTableWidget(0, 7)
        self.tbl_search.setHorizontalHeaderLabels(
            ["ID", "Morada", "Preço", "Quartos", "WC", "Área", "Localização"]
        )

        root.addLayout(linha_texto)
        root.addLayout(linha_local)
        root.addWidget(self.tbl_search)
        self.tab_pesquisar.setLayout(root)

        try:
            self._popular_distritos()
        except Exception as exc:
            QMessageBox.warning(self, "Aviso", f"Não foi possível carregar distritos:\n{exc}")

    def _popular_distritos(self):
        self.search_distrito.blockSignals(True)
        self.search_distrito.clear()
        self.search_distrito.addItem("Todos", None)

        distritos = self.repo.listar_distritos()
        for distrito in distritos:
            self.search_distrito.addItem(distrito["nome"], distrito["id_distrito"])

        self.search_distrito.blockSignals(False)
        self._reset_concelhos()
        self._reset_freguesias()

    def _reset_concelhos(self):
        self.search_concelho.blockSignals(True)
        self.search_concelho.clear()
        self.search_concelho.addItem("Todos", None)
        self.search_concelho.blockSignals(False)

    def _reset_freguesias(self):
        self.search_freguesia.clear()
        self.search_freguesia.addItem("Todos", None)

    def _on_distrito_changed(self):
        id_distrito = self._selected_combo_id(self.search_distrito)
        self._reset_concelhos()
        self._reset_freguesias()

        if not id_distrito:
            return

        concelhos = self.repo.listar_concelhos_por_distrito(id_distrito)
        self.search_concelho.blockSignals(True)
        for concelho in concelhos:
            self.search_concelho.addItem(concelho["nome"], concelho["id_concelho"])
        self.search_concelho.blockSignals(False)

    def _on_concelho_changed(self):
        id_concelho = self._selected_combo_id(self.search_concelho)
        self._reset_freguesias()

        if not id_concelho:
            return

        freguesias = self.repo.listar_freguesias_por_concelho(id_concelho)
        for freguesia in freguesias:
            self.search_freguesia.addItem(freguesia["nome"], freguesia["id_freguesia"])

    @staticmethod
    def _selected_combo_id(combo: QComboBox):
        return combo.currentData()

    def _build_criar_tab(self):
        root = QVBoxLayout()
        form = QFormLayout()

        self.in_morada = QLineEdit()
        self.in_preco = QLineEdit()
        self.in_desc = QLineEdit()
        self.in_quartos = QLineEdit("0")
        self.in_wc = QLineEdit("0")
        self.in_area = QLineEdit()
        self.create_anunciante = QComboBox()

        self.create_distrito = QComboBox()
        self.create_concelho = QComboBox()
        self.create_freguesia = QComboBox()

        self.create_distrito.currentIndexChanged.connect(self._on_criar_distrito_changed)
        self.create_concelho.currentIndexChanged.connect(self._on_criar_concelho_changed)

        form.addRow("Morada*", self.in_morada)
        form.addRow("Preço*", self.in_preco)
        form.addRow("Descrição", self.in_desc)
        form.addRow("Quartos", self.in_quartos)
        form.addRow("WC", self.in_wc)
        form.addRow("Área*", self.in_area)
        form.addRow("Anunciante (Nome - Email - Tipo)*", self.create_anunciante)
        form.addRow("Distrito*", self.create_distrito)
        form.addRow("Concelho*", self.create_concelho)
        form.addRow("Freguesia*", self.create_freguesia)

        btn_create = QPushButton("Criar anúncio")
        btn_create.clicked.connect(self._criar_anuncio)

        root.addLayout(form)
        root.addWidget(btn_create)
        self.tab_criar.setLayout(root)

        try:
            self._popular_distritos_criar()
        except Exception as exc:
            QMessageBox.warning(self, "Aviso", f"Não foi possível carregar localizações do formulário:\n{exc}")

        try:
            self._popular_anunciantes_criar()
        except Exception as exc:
            QMessageBox.warning(self, "Aviso", f"Não foi possível carregar anunciantes:\n{exc}")

    def _popular_anunciantes_criar(self):
        self.create_anunciante.clear()
        self.create_anunciante.addItem("Selecione", None)

        anunciantes = self.repo.listar_anunciantes()
        for anunciante in anunciantes:
            nome = anunciante.get("nome", "Sem nome")
            email = anunciante.get("email", "Sem email")
            tipo_label = anunciante.get("tipo_label", "Tipo desconhecido")
            label = f"{nome} - {email} - {tipo_label}"
            self.create_anunciante.addItem(label, anunciante["id_anunciante"])

    def _popular_distritos_criar(self):
        self.create_distrito.blockSignals(True)
        self.create_distrito.clear()
        self.create_distrito.addItem("Selecione", None)

        distritos = self.repo.listar_distritos()
        for distrito in distritos:
            self.create_distrito.addItem(distrito["nome"], distrito["id_distrito"])

        self.create_distrito.blockSignals(False)
        self._reset_concelhos_criar()
        self._reset_freguesias_criar()

    def _reset_concelhos_criar(self):
        self.create_concelho.blockSignals(True)
        self.create_concelho.clear()
        self.create_concelho.addItem("Selecione", None)
        self.create_concelho.blockSignals(False)

    def _reset_freguesias_criar(self):
        self.create_freguesia.clear()
        self.create_freguesia.addItem("Selecione", None)

    def _on_criar_distrito_changed(self):
        id_distrito = self._selected_combo_id(self.create_distrito)
        self._reset_concelhos_criar()
        self._reset_freguesias_criar()

        if not id_distrito:
            return

        concelhos = self.repo.listar_concelhos_por_distrito(id_distrito)
        self.create_concelho.blockSignals(True)
        for concelho in concelhos:
            self.create_concelho.addItem(concelho["nome"], concelho["id_concelho"])
        self.create_concelho.blockSignals(False)

    def _on_criar_concelho_changed(self):
        id_concelho = self._selected_combo_id(self.create_concelho)
        self._reset_freguesias_criar()

        if not id_concelho:
            return

        freguesias = self.repo.listar_freguesias_por_concelho(id_concelho)
        for freguesia in freguesias:
            self.create_freguesia.addItem(freguesia["nome"], freguesia["id_freguesia"])

    def _carregar_lista(self):
        try:
            data = self.repo.listar_imoveis()
            self._fill_table(self.tbl_listar, data, with_local=True)
        except Exception as exc:
            QMessageBox.critical(self, "Erro", f"Falha ao listar imóveis:\n{exc}")

    def _pesquisar(self):
        text = self.search_text.text().strip()
        preco_txt = self.search_preco_max.text().strip()
        preco_max = None

        if preco_txt:
            try:
                preco_max = float(preco_txt)
            except ValueError:
                QMessageBox.warning(self, "Validação", "Preço máximo inválido")
                return

        try:
            data = self.repo.pesquisar_imoveis(
                text,
                preco_max,
                self._selected_combo_id(self.search_distrito),
                self._selected_combo_id(self.search_concelho),
                self._selected_combo_id(self.search_freguesia),
            )
            self._fill_table(self.tbl_search, data, with_local=True)
        except Exception as exc:
            QMessageBox.critical(self, "Erro", f"Falha na pesquisa:\n{exc}")

    def _criar_anuncio(self):
        try:
            id_anunciante = self._selected_combo_id(self.create_anunciante)
            id_freguesia = self._selected_combo_id(self.create_freguesia)

            if not id_anunciante:
                raise ValueError("Selecione um anunciante")
            if not id_freguesia:
                raise ValueError("Selecione uma freguesia")

            payload = {
                "morada": self.in_morada.text().strip(),
                "preco": Decimal(self.in_preco.text().strip()),
                "descricao": self.in_desc.text().strip() or None,
                "numero_quartos": int(self.in_quartos.text().strip() or "0"),
                "numero_wc": int(self.in_wc.text().strip() or "0"),
                "area": Decimal(self.in_area.text().strip()),
                "id_anunciante": id_anunciante,
                "id_freguesia": id_freguesia,
            }
            if not payload["morada"]:
                raise ValueError("Morada é obrigatória")

            novo_id = self.repo.criar_anuncio(payload)
            QMessageBox.information(self, "Sucesso", f"Anúncio criado com ID {novo_id}")
            self._carregar_lista()
        except Exception as exc:
            QMessageBox.critical(self, "Erro", f"Não foi possível criar anúncio:\n{exc}")

    def _fill_table(self, table: QTableWidget, rows: list[dict], with_local: bool):
        table.setRowCount(0)
        for row_idx, row in enumerate(rows):
            table.insertRow(row_idx)
            table.setItem(row_idx, 0, QTableWidgetItem(str(row.get("id_imovel", ""))))
            table.setItem(row_idx, 1, QTableWidgetItem(str(row.get("morada", ""))))
            table.setItem(row_idx, 2, QTableWidgetItem(str(row.get("preco", ""))))
            table.setItem(row_idx, 3, QTableWidgetItem(str(row.get("numero_quartos", ""))))
            table.setItem(row_idx, 4, QTableWidgetItem(str(row.get("numero_wc", ""))))
            table.setItem(row_idx, 5, QTableWidgetItem(str(row.get("area", ""))))

            if with_local:
                local = f"{row.get('freguesia', '')}, {row.get('concelho', '')}, {row.get('distrito', '')}"
                table.setItem(row_idx, 6, QTableWidgetItem(local))
