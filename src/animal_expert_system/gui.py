"""Optional PyQt5 desktop user interface."""

from __future__ import annotations

import sys

from .engine import ForwardChainingEngine
from .knowledge_base import load_knowledge_base


def run_gui() -> int:
    try:
        from PyQt5 import QtCore, QtWidgets
    except ImportError as exc:
        raise SystemExit(
            "PyQt5 is not installed. Run `pip install -e .[gui]` or use the CLI."
        ) from exc

    kb = load_knowledge_base()
    engine = ForwardChainingEngine(kb)

    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("Animal Expert System / 动物识别专家系统")
            self.resize(980, 720)
            self._checks: dict[int, QtWidgets.QCheckBox] = {}
            self._build_ui()

        def _build_ui(self) -> None:
            central = QtWidgets.QWidget()
            root = QtWidgets.QVBoxLayout(central)

            title = QtWidgets.QLabel("Rule-Based Animal Identification Expert System")
            title.setAlignment(QtCore.Qt.AlignCenter)
            title.setStyleSheet("font-size: 22px; font-weight: 600; margin: 8px;")
            root.addWidget(title)

            subtitle = QtWidgets.QLabel(
                "Select observable features, then run forward-chaining inference.\n"
                "选择可观察特征，然后运行正向链式推理。"
            )
            subtitle.setAlignment(QtCore.Qt.AlignCenter)
            root.addWidget(subtitle)

            body = QtWidgets.QHBoxLayout()
            root.addLayout(body, 1)

            feature_box = QtWidgets.QGroupBox("Observable features / 可观察特征")
            feature_layout = QtWidgets.QGridLayout(feature_box)
            for index, concept in enumerate(kb.observable):
                checkbox = QtWidgets.QCheckBox(
                    f"{concept.id}. {concept.en} / {concept.zh}"
                )
                self._checks[concept.id] = checkbox
                feature_layout.addWidget(checkbox, index // 2, index % 2)
            body.addWidget(feature_box, 1)

            output_box = QtWidgets.QGroupBox("Inference / 推理结果")
            output_layout = QtWidgets.QVBoxLayout(output_box)
            self.result_label = QtWidgets.QLabel("No result yet / 尚未推理")
            self.result_label.setWordWrap(True)
            self.result_label.setStyleSheet("font-size: 18px; font-weight: 600;")
            output_layout.addWidget(self.result_label)

            self.trace = QtWidgets.QPlainTextEdit()
            self.trace.setReadOnly(True)
            output_layout.addWidget(self.trace, 1)
            body.addWidget(output_box, 1)

            buttons = QtWidgets.QHBoxLayout()
            infer_button = QtWidgets.QPushButton("Infer / 推理")
            infer_button.clicked.connect(self._infer)
            reset_button = QtWidgets.QPushButton("Reset / 重置")
            reset_button.clicked.connect(self._reset)
            buttons.addStretch(1)
            buttons.addWidget(infer_button)
            buttons.addWidget(reset_button)
            root.addLayout(buttons)

            self.setCentralWidget(central)

        def _infer(self) -> None:
            facts = [concept_id for concept_id, box in self._checks.items() if box.isChecked()]
            result = engine.infer(facts)

            if result.animals:
                names = [kb.format_concept(x, "bilingual") for x in result.animals]
                self.result_label.setText("Result / 结果: " + ", ".join(names))
            else:
                self.result_label.setText(
                    "Result / 结果: insufficient facts to identify an animal / 特征不足，无法识别"
                )

            lines: list[str] = []
            for step in result.steps:
                premises = ", ".join(kb.format_concept(x, "bilingual") for x in step.premises)
                conclusion = kb.format_concept(step.conclusion, "bilingual")
                lines.append(f"{step.rule_id}: IF {premises}\n    THEN {conclusion}")
            self.trace.setPlainText("\n\n".join(lines) if lines else "No rule fired / 没有规则被触发")

        def _reset(self) -> None:
            for box in self._checks.values():
                box.setChecked(False)
            self.result_label.setText("No result yet / 尚未推理")
            self.trace.clear()

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(run_gui())
