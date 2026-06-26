
LaTeX — math cheat sheet (Aaron-Cuevas)

  COMPILE (from the terminal)
    latexmk -pdf file.tex             best: handles passes + bib
    latexmk -c                        clean the .aux/.log leftovers
    pdflatex file.tex                 fallback (run it twice)

  MINIMAL SKELETON
    \documentclass[11pt]{article}
    \usepackage{amsmath,amssymb}
    \begin{document}
      ...
    \end{document}

  MATH MODES
    inline            $E = mc^2$
    display           \[ E = mc^2 \]
    numbered          \begin{equation} ... \end{equation}
    aligned           \begin{align} a &= b \\ &= c \end{align}

  COMMON
    sub / super       x_i      x^{2}     x_{i}^{2}
    greek             \alpha \beta \gamma \lambda \omega \Omega \nabla
    fractions/roots   \frac{a}{b}   \sqrt{x}   \sqrt[n]{x}
    sums/integrals    \sum_{i=1}^{n}   \int_a^b f\,dx   \lim_{x\to 0}
    operators         \cdot \times \approx \propto \partial \nabla \infty
    vectors           \vec{v}   \hat{n}   \mathbf{E}
    matrices          \begin{pmatrix} a & b \\ c & d \end{pmatrix}

  physics PACKAGE  (\usepackage{physics})
    derivatives       \dv{f}{x}     \pdv{\psi}{t}     \dv[2]{x}{t}
    bra-ket           \bra{\psi}    \ket{\phi}    \braket{\psi}{\phi}
    abs / norm        \abs{x}       \norm{v}

  siunitx PACKAGE  (\usepackage{siunitx})
    quantity          \SI{632.8}{nm}      \SI{3e8}{m/s}
    unit only         \si{\meter\per\second}
    number only       \num{6.022e23}

  FIGURES / REFS
    \begin{figure}[h]\centering
      \includegraphics[width=.6\linewidth]{img.png}
      \caption{...}\label{fig:x}
    \end{figure}
    refer to it       Fig.~\ref{fig:x},  Eq.~\eqref{eq:x}

  CAN'T REMEMBER A SYMBOL?  draw it at detexify (see resources) -> get the command.
