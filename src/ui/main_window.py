from __future__ import annotations

from decimal import Decimal

from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QHeaderView,
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


APP_STYLESHEET = """
QMainWindow {
    background-color: #F5F1E8;
}

QWidget {
    font-family: 'Segoe UI';
    font-size: 13px;
    color: #1F2A44;
}

QTabWidget::pane {
    border: 1px solid #B9C8DA;
    border-radius: 10px;
    background: #FFFDF8;
    top: -1px;
}

QTabBar::tab {
    background: #D8E6F5;
    color: #163A5F;
    padding: 8px 14px;
    border: 1px solid #AAC0D8;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
}

QTabBar::tab:selected {
    background: #2F5D8A;
    color: #FFFFFF;
}

QLineEdit, QComboBox {
    background: #FFFFFF;
    border: 1px solid #B8C7D9;
    border-radius: 8px;
    padding: 6px 8px;
    min-height: 28px;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #2F5D8A;
}

QPushButton {
    background-color: #4A78A8;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #3B6691;
}

QPushButton:pressed {
    background-color: #2D5277;
}

QPushButton#secondaryButton {
    background-color: #E0D6C2;
    color: #2E3C52;
}

QPushButton#secondaryButton:hover {
    background-color: #D3C6AD;
}

QTableWidget {
    background: #FFFFFF;
    alternate-background-color: #F4F8FC;
    border: 1px solid #B9C8DA;
    border-radius: 8px;
    gridline-color: #D6E0EA;
    selection-background-color: #D8E6F5;
    selection-color: #1F2A44;
}

QHeaderView::section {
    background-color: #2F5D8A;
    color: #FFFFFF;
    border: none;
    padding: 6px;
    font-weight: 600;
}

QLabel {
    color: #244365;
    font-weight: 600;
}

QLabel#portalTitle {
    color: #1F3F63;
    font-size: 24px;
    font-weight: 700;
}

QLabel#portalSubtitle {
    color: #4F6A86;
    font-size: 13px;
    font-weight: 500;
}

QLabel#resultsCounter {
    color: #2F5D8A;
    font-size: 12px;
    font-weight: 700;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.repo = ImovelRepository()

        self.setWindowTitle("Imociccopn - Gestão de Imóveis")
        self.resize(1200, 800)

        central = QWidget()
        self.central_layout = QVBoxLayout(central)
        self.central_layout.setContentsMargins(16, 14, 16, 16)
        self.central_layout.setSpacing(10)

        self.tabs = QTabWidget()
        self.central_layout.addWidget(self._build_header())
        self.central_layout.addWidget(self.tabs)

        self.setCentralWidget(central)
        self.setStyleSheet(APP_STYLESHEET)

        self.tab_listar = QWidget()
        self.tab_pesquisar = QWidget()
        self.tab_criar = QWidget()

        self.tabs.addTab(self.tab_listar, "Listar")
        self.tabs.addTab(self.tab_pesquisar, "Pesquisar")
        self.tabs.addTab(self.tab_criar, "Criar anúncio")

        self._build_listar_tab()
        self._build_pesquisar_tab()
        self._build_criar_tab()
        self._apply_visual_tweaks()

    def _build_header(self) -> QWidget:
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(6, 2, 6, 4)
        header_layout.setSpacing(2)

        title = QLabel("Imociccopn — Portal Imobiliário")
        subtitle = QLabel("Pesquisa e gestão de anúncios de imóveis")
        title.setObjectName("portalTitle")
        subtitle.setObjectName("portalSubtitle")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        return header

    def _apply_visual_tweaks(self):
        self.btn_refresh.setObjectName("secondaryButton")
        self._configurar_tabela(self.tbl_listar)
        self._configurar_tabela(self.tbl_search)

    @staticmethod
    def _configurar_tabela(table: QTableWidget):
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.setFrameShape(QFrame.Shape.NoFrame)
        table.setShowGrid(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

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
        linha_precos_areas = QHBoxLayout()
        linha_specs = QHBoxLayout()
        linha_local = QHBoxLayout()

        self.search_text = QLineEdit()
        self.search_text.setPlaceholderText("morada ou descrição")
        self.search_preco_min = QLineEdit()
        self.search_preco_min.setPlaceholderText("preço mínimo (opcional)")
        self.search_preco_max = QLineEdit()
        self.search_preco_max.setPlaceholderText("preço máximo (opcional)")
        self.search_area_min = QLineEdit()
        self.search_area_min.setPlaceholderText("área mínima (opcional)")
        self.search_area_max = QLineEdit()
        self.search_area_max.setPlaceholderText("área máxima (opcional)")

        self.search_tipologia = QComboBox()
        self.search_tipologia.addItem("Todas", None)
        for i in range(6):
            self.search_tipologia.addItem(f"T{i}", i)

        self.search_wc = QComboBox()
        self.search_wc.addItem("Todos", None)
        for i in range(6):
            self.search_wc.addItem(str(i), i)

        self.search_distrito = QComboBox()
        self.search_concelho = QComboBox()
        self.search_freguesia = QComboBox()

        self.search_distrito.currentIndexChanged.connect(self._on_distrito_changed)
        self.search_concelho.currentIndexChanged.connect(self._on_concelho_changed)

        btn_search = QPushButton("Pesquisar")
        btn_search.clicked.connect(self._pesquisar)
        btn_clear = QPushButton("Limpar filtros")
        btn_clear.setObjectName("secondaryButton")
        btn_clear.clicked.connect(self._limpar_filtros_pesquisa)

        linha_texto.addWidget(QLabel("Texto:"))
        linha_texto.addWidget(self.search_text)

        linha_precos_areas.addWidget(QLabel("Preço mín:"))
        linha_precos_areas.addWidget(self.search_preco_min)
        linha_precos_areas.addWidget(QLabel("Preço máx:"))
        linha_precos_areas.addWidget(self.search_preco_max)
        linha_precos_areas.addWidget(QLabel("Área mín:"))
        linha_precos_areas.addWidget(self.search_area_min)
        linha_precos_areas.addWidget(QLabel("Área máx:"))
        linha_precos_areas.addWidget(self.search_area_max)

        linha_specs.addWidget(QLabel("Tipologia:"))
        linha_specs.addWidget(self.search_tipologia)
        linha_specs.addWidget(QLabel("WC:"))
        linha_specs.addWidget(self.search_wc)

        linha_local.addWidget(QLabel("Distrito:"))
        linha_local.addWidget(self.search_distrito)
        linha_local.addWidget(QLabel("Concelho:"))
        linha_local.addWidget(self.search_concelho)
        linha_local.addWidget(QLabel("Freguesia:"))
        linha_local.addWidget(self.search_freguesia)
        linha_local.addWidget(btn_search)
        linha_local.addWidget(btn_clear)

        self.tbl_search = QTableWidget(0, 7)
        self.tbl_search.setHorizontalHeaderLabels(
            ["ID", "Morada", "Preço", "Quartos", "WC", "Área", "Localização"]
        )
        self.search_results_label = QLabel("Resultados encontrados: 0")
        self.search_results_label.setObjectName("resultsCounter")

        root.addLayout(linha_texto)
        root.addLayout(linha_precos_areas)
        root.addLayout(linha_specs)
        root.addLayout(linha_local)
        root.addWidget(self.search_results_label)
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
        preco_min_txt = self.search_preco_min.text().strip()
        preco_txt = self.search_preco_max.text().strip()
        area_min_txt = self.search_area_min.text().strip()
        area_max_txt = self.search_area_max.text().strip()

        preco_min = None
        preco_max = None
        area_min = None
        area_max = None

        if preco_min_txt:
            try:
                preco_min = float(preco_min_txt)
            except ValueError:
                QMessageBox.warning(self, "Validação", "Preço mínimo inválido")
                return

        if preco_txt:
            try:
                preco_max = float(preco_txt)
            except ValueError:
                QMessageBox.warning(self, "Validação", "Preço máximo inválido")
                return

        if area_min_txt:
            try:
                area_min = float(area_min_txt)
            except ValueError:
                QMessageBox.warning(self, "Validação", "Área mínima inválida")
                return

        if area_max_txt:
            try:
                area_max = float(area_max_txt)
            except ValueError:
                QMessageBox.warning(self, "Validação", "Área máxima inválida")
                return

        if preco_min is not None and preco_max is not None and preco_min > preco_max:
            QMessageBox.warning(self, "Validação", "Preço mínimo não pode ser maior que o preço máximo")
            return

        if area_min is not None and area_max is not None and area_min > area_max:
            QMessageBox.warning(self, "Validação", "Área mínima não pode ser maior que a área máxima")
            return

        try:
            data = self.repo.pesquisar_imoveis(
                texto=text,
                preco_min=preco_min,
                preco_max=preco_max,
                area_min=area_min,
                area_max=area_max,
                tipologia=self._selected_combo_id(self.search_tipologia),
                numero_wc=self._selected_combo_id(self.search_wc),
                id_distrito=self._selected_combo_id(self.search_distrito),
                id_concelho=self._selected_combo_id(self.search_concelho),
                id_freguesia=self._selected_combo_id(self.search_freguesia),
            )
            self._fill_table(self.tbl_search, data, with_local=True)
            self._atualizar_contador_resultados(len(data))
        except Exception as exc:
            QMessageBox.critical(self, "Erro", f"Falha na pesquisa:\n{exc}")

    def _limpar_filtros_pesquisa(self):
        self.search_text.clear()
        self.search_preco_min.clear()
        self.search_preco_max.clear()
        self.search_area_min.clear()
        self.search_area_max.clear()
        self.search_tipologia.setCurrentIndex(0)
        self.search_wc.setCurrentIndex(0)
        self.search_distrito.setCurrentIndex(0)
        self.search_concelho.setCurrentIndex(0)
        self.search_freguesia.setCurrentIndex(0)
        self.tbl_search.setRowCount(0)
        self._atualizar_contador_resultados(0)

    def _atualizar_contador_resultados(self, total: int):
        self.search_results_label.setText(f"Resultados encontrados: {total}")

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
