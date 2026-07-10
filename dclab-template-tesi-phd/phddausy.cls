\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{phddausy}[2020/11/06 Class for PhD theses at DAUSY]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CLASS OPTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Language
\DeclareOption{american} { \def \phddausy@thesis{Dissertation} }
\DeclareOption{USenglish}{ \def \phddausy@thesis{Dissertation} }
\DeclareOption{english}  { \def \phddausy@thesis{Thesis} }
\DeclareOption{UKenglish}{ \def \phddausy@thesis{Thesis} }

%% Colophon
\DeclareOption{colophon}  { \def \phddausy@colophon{true}  }
\DeclareOption{nocolophon}{ \def \phddausy@colophon{false} }

%% Screen mode
\DeclareOption{screen}
{
    \AtBeginDocument
    {
        \@ifpackageloaded{url}
            {\urlstyle{same}}
            {\ClassWarningNoLine{phddausy}{Package 'url' missing}}
        \@ifpackageloaded{hyperref}
            {\hypersetup{colorlinks, allcolors = dausylink}}
            {\ClassWarningNoLine{phddausy}{Package 'hyperref' missing}}
        \setlrmarginsandblock{24.35mm}{24.35mm}{*}
        \checkandfixthelayout
    }
}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{memoir}}

\ExecuteOptions{UKenglish}
\ExecuteOptions{nocolophon}
\ProcessOptions
\relax

\LoadClass[oldfontcommands, extrafontsizes]{memoir}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PACKAGES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage{keyval}
\RequirePackage{etoolbox}
\RequirePackage{textcomp}
\RequirePackage[dvipsnames, svgnames, cmyk]{xcolor}
\RequirePackage{pdfpages}
\RequirePackage{graphicx}
\graphicspath{{figures/}}
\RequirePackage{tikz}
\usetikzlibrary{calc}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LAYOUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Paper size
% \setstocksize{240mm}{170mm}
% \settrimmedsize{240mm}{170mm}{*}

\setstocksize{297mm}{210mm}
\settrimmedsize{297mm}{210mm}{*}

\settrims{0mm}{0mm}
\setlrmarginsandblock{40mm}{35mm}{*}
\setulmarginsandblock{30mm}{35mm}{*}
\checkandfixthelayout

%% Custom title page
\newcommand{\dausytitle}
{
    \begin{titlingpage}
        \sffamily
        \renewcommand{\and}{\vskip1mm}
        \newcommand{\AND}{\vskip9mm}
        \calccentering{\unitlength}
        \begin{adjustwidth*}{\unitlength}{}
            \raggedright
            \vspace*{-5mm}
            \includegraphics[width = 0.25\textwidth]{figures/dausy.png}
            \vskip25mm
            \resizebox
            {
                \ifdim \width > \textwidth
                \textwidth
                \else
                \width
                \fi
            }{!}
            {%
                \Large
                \theauthor
            }
            \vskip1\onelineskip
            {
                \Huge
                \bfseries
                \boldmath
                \thetitle
                \par
            }
            {
                \ifcsempty{\phddausy@subtitle}
                {}
                {
                    \vskip2mm
                    \huge
                    \phddausy@subtitle
                    \par
                }
            }
            \vskip-\lastskip
            \vskip16mm
            \resizebox{\textwidth}{!}
            {%
                \bfseries
                \phddausy@thesis\
                submitted for the degree of Philosophiae Doctor
            }
            \AND
            {
                \normalsize
                \phddausy@dept\
                \and
                \phddausy@faculty\
                \AND
                \phddausy@affiliation\
            }
            \vfill
            \begin{minipage}[c][26mm]{28mm}
                \hspace*{0mm}
                \includegraphics[height = 30mm]{figures/poliLogo.pdf}
            \end{minipage}%
            \begin{minipage}[c][26mm]{28mm}
                \hspace*{5mm}
                \includegraphics[height = 30mm]{figures/uniLogo.png}
            \end{minipage}%
            \begin{minipage}[c]{\textwidth - 58mm}
                \hfill
                \LARGE
                \bfseries
                \phddausy@ayear
            \end{minipage}
            \vspace{2mm}
        \end{adjustwidth*}

        \null
    \end{titlingpage}
}

%% Book
\renewcommand*{\printbooktitle}[1]{\raggedright\booktitlefont #1}
\renewcommand*{\afterbookskip}{\par}
\renewcommand*{\booktitlefont}{\HUGE\bfseries\boldmath\sffamily}
\renewcommand*{\booknamefont}{\raggedright\Huge\normalfont\sffamily}
\renewcommand*{\booknumfont}{\Huge\normalfont\sffamily}


%% Part
\renewcommand*{\printparttitle}[1]{\raggedright\parttitlefont #1}
\renewcommand*{\afterpartskip}{\par}
\renewcommand*{\parttitlefont}{\HUGE\bfseries\boldmath\sffamily}
\renewcommand*{\partnamefont}{\raggedright\Huge\normalfont\sffamily}
\renewcommand*{\partnumfont}{\Huge\normalfont\sffamily}

%% Chapter
\newcommand{\authorsfont}{}
\newcommand{\metadatafont}{}
\newlength{\afterauthorsskip}
\newlength{\aftermetadataskip}

\makechapterstyle{phddausy}
{
    \renewcommand*{\chapnamefont}{\huge\sffamily}
    \renewcommand*{\chapnumfont}{\huge\sffamily}
    \renewcommand*{\chaptitlefont}
    {\Huge\bfseries\boldmath\sffamily\raggedright}
    \renewcommand*{\authorsfont}{\Large\bfseries\sffamily}
    \renewcommand*{\metadatafont}{\normalfont\normalsize\sffamily}

    \setlength{\beforechapskip}{-1.35\baselineskip}
    \setlength{\midchapskip}{10pt}
    \setlength{\afterchapskip}{20pt}
    \setlength{\afterauthorsskip}{6pt}
    \setlength{\aftermetadataskip}{15pt}

    \renewcommand*{\afterchaptertitle}
    {
        \vskip\afterchapskip
        \ifboolexpr
        {
            test{ \ifcsempty{phddausy@authors} }
            and
            test{ \ifcsempty{phddausy@metadata} }
        }
        {}
        {
        \begin{minipage}[t]{\textwidth}
            \authorsfont
            \phddausy@authors
            \vskip\afterauthorsskip
            \metadatafont
            \phddausy@metadata
            \gdef \phddausy@authors{}
            \gdef \phddausy@metadata{}
        \end{minipage}
        \vskip\aftermetadataskip
        }
    }

    \renewcommand*{\printchapternonum}
    {
        \vphantom{\chapnumfont Chapter}
        \afterchapternum
        \vskip\topskip
    }
}

\chapterstyle{phddausy}


%% Lower level sections
\setsecnumdepth{subsubsection}
\setsecheadstyle{\Large\bfseries\boldmath\sffamily\raggedright}
\setsubsecheadstyle{\large\bfseries\boldmath\sffamily\raggedright}
\setsubsubsecheadstyle{\normalsize\bfseries\boldmath\sffamily\raggedright}
\setparaheadstyle{\normalsize\bfseries\boldmath\sffamily\raggedright}
\setsubparaheadstyle{\normalsize\bfseries\boldmath\sffamily\raggedright}

%% Subappendices
\namedsubappendices

%% Abstract
\renewcommand{\abstractnamefont}{\sffamily\bfseries}
\renewcommand{\abstracttextfont}{\normalfont\small\noindent\ignorespaces}

%% Table of contents, list of figures and list of tables
\setrmarg{3em}
\setpnumwidth{2em}
\addtolength{\cftfigurenumwidth}{1em}
\addtolength{\cfttablenumwidth}{1em}
\addtolength{\cftbooknumwidth}{1em}
\addtolength{\cftpartnumwidth}{1em}
\addtolength{\cftchapternumwidth}{1em}
\addtolength{\cftsectionnumwidth}{1em}
\addtolength{\cftsubsectionnumwidth}{1em}
\addtolength{\cftsubsubsectionnumwidth}{1em}
\addtolength{\cftparagraphnumwidth}{1em}
\addtolength{\cftsubparagraphnumwidth}{1em}
\addtolength{\cftsectionindent}{1em}
\addtolength{\cftsubsectionindent}{2em}
\addtolength{\cftsubsubsectionindent}{3em}
\addtolength{\cftparagraphindent}{4em}
\addtolength{\cftsubparagraphindent}{5em}
\renewcommand{\cftchapteraftersnumb}{\bfseries\boldmath}


%% Running header and footer
\makepagestyle{phddausy}
\makeheadrule{phddausy}{\textwidth}{\normalrulethickness}
\makeevenhead{phddausy}{\sffamily\leftmark}{}{}
\makeoddhead {phddausy}{}{}{\sffamily\rightmark}
\makeevenfoot{phddausy}{\sffamily\thepage}{}{}
\makeoddfoot {phddausy}{}{}{\sffamily\thepage}
\makepsmarks{phddausy}
{
    \nouppercaseheads
    \createmark{chapter}{left}{shownumber}{}{. \space}
    \createmark{section}{right}{nonumber}{}{}
    \createplainmark{toc}{both}{\contentsname}
    \createplainmark{lof}{both}{\listfigurename}
    \createplainmark{lot}{both}{\listtablename}
    \createplainmark{bib}{both}{\bibname}
    \createplainmark{index}{both}{\indexname}
    \createplainmark{glossary}{both}{\glossaryname}
}
\pagestyle{phddausy}

\makepagestyle{chapter}
\makeevenfoot{chapter}{\sffamily\thepage}{}{}
\makeoddfoot {chapter}{}{}{\sffamily\thepage}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% INCLUDE PAPERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Title for papers
\renewcommand{\maketitle}
{
    % \paperauthors{\theauthor}
    \edef\papertitle{{\thetitle}}
    \expandafter\chapter\papertitle
    \paperthumb
    % \saythanks
}


%% Specify authors for separate paper
\newcommand{\paperauthors}[1]
{
    \renewcommand{\and}{\leavevmode\unskip,\space}
    \def \phddausy@authors{#1}
}
\paperauthors{}


%% Specify metadata for separate paper
\newcommand{\metadata}[1]{ \def \phddausy@metadata{#1} }
\metadata{}

% Rename 'Chapter' to 'Paper'
\newcommand*{\paper}
{
    \setcounter{chapter}{0}
    \setcounter{section}{0}
    \ifdef{\theHchapter}
    {
        \renewcommand{\theHchapter}{papter.\arabic{chapter}}
    }
    {}
    \def \@chapapp{Paper}
    \let \c@paper \c@chapter
    \def \thechapter{\@Roman\c@chapter}
    \let \thepaper \thechapter
    \ifdef{\memendofchapterhook}
    {
        \renewcommand{\memendofchapterhook}
        {
            \addtocounter{paper}{-1}
            \refstepcounter{paper}
        }
    }
    {}
}
\newcounter{paper}

%% Standard \appendix is broken by \paper
%% Fix hyperlinks to appendices
\renewcommand*{\appendix}
{
    \setcounter{chapter}{0}
    \setcounter{section}{0}
    \ifdef{\theHchapter}
    {
        \renewcommand{\theHchapter}{\arabic{chapter}}
    }
    {}
    \def \@chapapp{\appendixname}
    \let \c@appendix \c@chapter
    \def \thechapter{\@Alph\c@chapter}
    \let \theappendix \thechapter
    \ifdef{\memendofchapterhook}
    {
        \renewcommand{\memendofchapterhook}
        {
            \addtocounter{appendix}{-1}
            \refstepcounter{appendix}
        }
    }
    {}
}
\newcounter{appendix}

%% Print 'Papers'
% \newcommand{\paperpage}
% {
%     \part*{Papers}
%     \addcontentsline{toc}{chapter}{Papers}
%     \cleartorecto
% }


%% Specify number of papers
\newcommand{\numberofpapers}[1]{ \setcounter{totpapernum}{#1} }

%% Thumb index to separate papers
\newcommand{\paperthumb}
{
    \ifnum \value{thumbpos} = \value{totpapernum}
    \setcounter{thumbpos}{0}
    \fi
    
    \stepcounter{thumbnum}
    \stepcounter{thumbpos}
    
    \pgfmathsetlength{\thumbheight}{\paperheight / \value{totpapernum}}
    
    \begin{tikzpicture}[remember picture, overlay]
        \node [thumb, align = right, anchor = north east]
        at
        ($(current page.north east) - (0,{(\value{thumbpos}-1)*\thumbheight})$)
        {\Roman{thumbnum}};
    \end{tikzpicture}
}

\newcounter{thumbnum}
\newcounter{thumbpos}
\newcounter{totpapernum}
\setcounter{totpapernum}{2}

\newlength{\thumbwidth}
\newlength{\thumbheight}
\setlength{\thumbwidth}{1cm}

\tikzset
{
    thumb/.style =
    {
        fill           = dausyblack,
        text           = dausywhite,
        font           = \sffamily\bfseries\Huge,
        text width     = \thumbwidth,
        minimum height = \thumbheight,
        outer sep      = 0pt,
        inner xsep     = 1.5em
    }
}

%% Unmarked footnote
\newcommand{\papernote}[1]
{
    \begingroup
        \renewcommand{\thefootnote}{}
        \footnotetext{#1}
     \endgroup
}

%% Unmarked footnote for paper title
\renewcommand{\thanks}[1]{ \gdef \phddausy@thanks{#1} }
\thanks{}
\renewcommand{\saythanks}
{
    \ifcsempty{phddausy@thanks}
    {}
    {
        \papernote{\phddausy@thanks}
        \thanks{}
    }
}


%% Include PDFs containing separate papers
%% Based on code by Dag Langmyhr
\newcommand{\includearticle}[2][]
{
    \cleartorecto

    \def \ps@default
    {
        \let \@mkboth\@gobbletwo
        \let \@oddhead\@empty
        \def \@oddfoot{\hfil\sffamily\thepage}
        \let \@evenhead\@empty
        \def \@evenfoot{\sffamily\thepage\hfil}
    }

    \def \phddausy@ps{default}

    \def \ps@low
    {
        \let\@mkboth\@gobbletwo
        \let\@oddhead\@empty
        \def\@oddfoot{\hfil\raisebox{-7.5mm}{\sffamily\thepage}}
        \let\@evenhead\@empty
        \def\@evenfoot{\raisebox{-7.5mm}{\sffamily\thepage}\hfil}
    }

    \let \ps@none = \ps@empty

    \setkeys{phddausy@keys}{#1}

    \includepdf[pages = {-}, pagecommand = {\thispagestyle{\phddausy@ps}}]{#2}
}

\define@key{phddausy@keys}{numbers}{ \def \phddausy@ps{#1} }


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% UTILITIES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Offical colours
\definecolor{dausyred}  {cmyk}{0, 1, 1, 0}
\definecolor{dausygrey} {cmyk}{0, 0.05, 0.1, 0.29}
\definecolor{dausywhite}{cmyk}{0, 0, 0, 0}
\definecolor{dausyblack}{cmyk}{0, 0, 0, 1}
\definecolor{dausylink} {HTML}{0B5A9D}

%% Subtitle
\newcommand{\subtitle}[1]{ \def \phddausy@subtitle{#1} }
\subtitle{}

%% Specify data
\newcommand{\department}[1]{ \def \phddausy@dept{#1} }
\newcommand{\faculty}[1]{ \def \phddausy@faculty{#1} }
\newcommand{\affiliation}[1]{ \def \phddausy@affiliation{#1} }
\newcommand{\ayear}[1]{ \def \phddausy@ayear{#1} }
\department{}
\faculty{}
\affiliation{}
\ayear{}

%% Print current month
\newcommand{\MONTH}
{%
    \leavevmode\unskip\space
    \ifcase\the\month
    \or January
    \or February
    \or March
    \or April
    \or May
    \or June
    \or July
    \or August
    \or September
    \or October
    \or November
    \or December
    \fi
    \ignorespaces
}
\endinput