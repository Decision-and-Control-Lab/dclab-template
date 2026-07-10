%% TEMPLATE TESINA ANALISI DEI SISTEMI 
%% 
%% Decision & Control Lab
%% Politecnico di Bari
%% 
%% Questo è un template per la redazione di tesine 
%% per il laboratorio di analisi dei sistemi.
%%
%% NON MODIFICARE i file presenti nella cartella 00-settings.
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Identificazione della classe
\ProvidesClass{00-settings/document}

% Pacchetti
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\RequirePackage[fit, breakall]{truncate}

% Opzioni della classe
\newif\if@color\@colorfalse
\newif\if@pdf\@pdffalse

\DeclareOption{color}{\@colortrue}
\DeclareOption{pdftex}{\@pdftrue}
\DeclareOption{twocolumn}{\OptionNotUsed}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\if@pdf
  \RequirePackage[pdftex]{graphicx}
\else
  \RequirePackage{graphicx}
\fi
\LoadClass[a4paper]{article}

% Margini
\topmargin -50mm
\headheight 60mm
\textheight 220mm
\textwidth 150mm
\hoffset -15mm
\leftmargin 15mm
\rightmargin 15mm

% Colori (attivi solo con l'opzione di classe "color")
\if@color
  \RequirePackage{color}
\fi

% Loghi di default (sovrascrivibili da main.tex con \renewcommand)
\providecommand{\logosinistra}{00-settings/LogoPoliBa_header.jpg}
\providecommand{\logodestra}{00-settings/LogoDandC.jpg}

% Intestazione
\pagestyle{fancy}
\lhead{\setlength{\unitlength}{1mm}{\includegraphics[height=15mm]{\logosinistra}}}
\chead{}
\rhead{\setlength{\unitlength}{1mm}{\includegraphics[height=15mm]{\logodestra}}}

\lfoot{\small \truncate{0.8\textwidth} \@title}
\cfoot{} 
\rfoot{{\footnotesize \thepage\ \textit{/} \pageref{LastPage}}}
\renewcommand{\footrulewidth}{0.4pt}%
