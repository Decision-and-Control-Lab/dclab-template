%% TEMPLATE RELAZIONE TIROCINIO
%%
%% Decision & Control Lab
%% Politecnico di Bari
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
\RequirePackage[default]{opensans}

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
\RequirePackage[a4paper, top=20mm, bottom=40mm, left=20mm, right=20mm]{geometry}

% Colori (attivi solo con l'opzione di classe "color")
\if@color
  \RequirePackage{color}
\fi

% Intestazione (i loghi del frontespizio sono gestiti da style.sty,
% qui il piè di pagina riporta solo titolo e numero di pagina)
\lfoot{\small \truncate{0.8\textwidth} \@title}
\cfoot{} 
\rfoot{{\footnotesize \thepage\ \textit{/} \pageref{LastPage}}}
\renewcommand{\footrulewidth}{0.4pt}%
