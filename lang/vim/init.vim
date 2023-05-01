:set tags=.tags;

:set shell=/bin/zsh
:set shiftwidth=4
:set tabstop=4
:set expandtab
:set textwidth=0
:set clipboard+=unnamed
:set tags=.tags;
:set cursorline
:set ignorecase
":set cursorcolumn

:set number
:set nowrapscan
:set nowrap
:set encoding=UTF-8

call plug#begin()
Plug 'ntk148v/vim-horizon'
Plug 'preservim/nerdtree'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'morhetz/gruvbox'
Plug 'Yggdroot/indentLine'
Plug 'vim-scripts/taglist.vim'
Plug 'ryanoasis/vim-devicons'
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
Plug 'jlanzarotta/bufexplorer'
"ddc系 
Plug 'vim-denops/denops.vim'
Plug 'Shougo/ddc.vim'
Plug 'Shougo/pum.vim'
Plug 'Shougo/ddc-around'
Plug 'LumaKernel/ddc-file'
Plug 'Shougo/ddc-matcher_head'
Plug 'Shougo/ddc-sorter_rank'
Plug 'Shougo/ddc-converter_remove_overlap'
Plug 'mattn/vim-lsp-settings'
Plug 'prabirshrestha/vim-lsp'
call plug#end()

"補完系
call plug#('Shougo/ddc.vim')
call plug#('vim-denops/denops.vim')
call plug#('Shougo/pum.vim')
call plug#('Shougo/ddc-around')
call plug#('LumaKernel/ddc-file')
call plug#('Shougo/ddc-matcher_head')
call plug#('Shougo/ddc-sorter_rank')
call plug#('Shougo/ddc-converter_remove_overlap')
call plug#('prabirshrestha/vim-lsp')
call plug#('mattn/vim-lsp-settings')

call ddc#custom#patch_global('completionMenu', 'pum.vim')
call ddc#custom#patch_global('sources', [
 \ 'around',
 \ 'vim-lsp',
 \ 'file'
 \ ])
call ddc#custom#patch_global('sourceOptions', {
 \ '_': {
 \   'matchers': ['matcher_head'],
 \   'sorters': ['sorter_rank'],
 \   'converters': ['converter_remove_overlap'],
 \ },
 \ 'around': {'mark': 'Around'},
 \ 'vim-lsp': {
 \   'mark': 'LSP', 
 \   'matchers': ['matcher_head'],
 \   'forceCompletionPattern': '\.|:|->|"\w+/*'
 \ },
 \ 'file': {
 \   'mark': 'file',
 \   'isVolatile': v:true, 
 \   'forceCompletionPattern': '\S/\S*'
 \ }})
call ddc#enable()
inoremap <Tab> <Cmd>call pum#map#insert_relative(+1)<CR>
inoremap <S-Tab> <Cmd>call pum#map#insert_relative(-1)<CR>

source ~/.vim/gtags.vim

"" if you don't set this option, this color might not correct
"set termguicolors
"colorscheme horizon
"" lightline
"let g:lightline = {}
"let g:lightline.colorscheme = 'horizon'
"" or this line
"let g:lightline = {'colorscheme' : 'horizon'}

"NERDTree
let NERDTreeShowHidden=1
nmap nf :NERDTreeFind<CR>
nmap nt :NERDTreeToggle<CR>
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 0 && !exists('s:std_in') | NERDTree | endif

"airline
let g:airline_powerline_fonts=1

"colorscheme
set background=dark
let g:gruvbox_contrast_dark="hard"
colorscheme gruvbox

"indentLine"
"let g:indentLine_color_term=239
"let g:indentLine_color_gui='#708090'
"let g:indentLine_char=':'

"taglist
let Tlist_Use_Right_Window=1

nmap <ESC><ESC> :nohlsearch<CR><ESC>

map <S-k> 20k
map <S-j> 20j
map <S-l> $
map <S-h> 0

nmap <F1> :Explore<CR>
nmap <F2> :BufExplorer<CR>
nmap <F3> :Files<CR>
nmap <F4> :Tlist<CR>
nmap <F8> :!ctags -R --languages=C,C++ -f .tags<CR> :!gtags -v<CR>

nmap t g<C-]>
nmap <S-t> <C-t>
nmap r :GtagsCursor<CR>
nmap f :cn<CR>
nmap <S-f> :cp<CR>

nmap wl <C-w>l
nmap wh <C-w>h
nmap wj <C-w>j
nmap wk <C-w>k
nmap wv :vsplit<CR> 
nmap ws :split<CR> 
nmap wc :quit<CR>
nmap <C-c> :qa!<CR>

nmap , <C-w><
nmap . <C-w>>

nmap <S-u> <C-r> 
