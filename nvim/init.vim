set encoding=utf-8
set number
syntax enable
set noswapfile
set scrolloff=7
set backspace=indent,eol,start
set clipboard+=unnamedplus
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set autoindent
set fileformat=unix

call plug#begin('~/.config/nvim/plugged')

Plug 'hzchirs/vim-material'
Plug 'jiangmiao/auto-pairs'
Plug 'scrooloose/nerdtree'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
call plug#end()

let g:material_style='oceanic'
set background=dark
colorscheme vim-material

let g:airline_theme='base16_ocean'

if (has("termguicolors"))
    set termguicolors
endif

"NerdTree
let mapleader = ' '
let NERDTreeQuitOnOpen=1
let g:NERDTreeeMinimalUI=1
nmap <C-Down> :NERDTreeToggle<CR>
"NerdTree tabs
let g:airline#extensions#tabline#enabled=1
let g:airline#extensions#labline#fnamemode=1
nmap <leader>p :bp<cr>
nmap <leader>n :bn<cr>
nmap <leader>d :bd<cr>
