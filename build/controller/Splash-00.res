tcl86t.dll      tk86t.dll       tk              __splash          ,   �   �  	   �   XVCRUNTIME140.dll tk\tk.tcl tcl86t.dll tk86t.dll tk\ttk\cursors.tcl tk\license.terms tk\ttk\fonts.tcl tk\ttk\ttk.tcl tk\text.tcl tk\ttk\utils.tcl proc _ipc_server {channel clientaddr clientport} {
set client_name [format <%s:%d> $clientaddr $clientport]
chan configure $channel \
-buffering none \
-encoding utf-8 \
-eofchar \x04 \
-translation cr
chan event $channel readable [list _ipc_caller $channel $client_name]
}
proc _ipc_caller {channel client_name} {
chan gets $channel cmd
if {[chan eof $channel]} {
chan close $channel
exit
} elseif {![chan blocked $channel]} {
if {[string match "update_text*" $cmd]} {
global status_text
set first [expr {[string first "(" $cmd] + 1}]
set last [expr {[string last ")" $cmd] - 1}]
set status_text [string range $cmd $first $last]
}
}
}
set server_socket [socket -server _ipc_server -myaddr localhost 0]
set server_port [fconfigure $server_socket -sockname]
set env(_PYIBoot_SPLASH) [lindex $server_port 2]
image create photo splash_image
splash_image put $_image_data
unset _image_data
proc canvas_text_update {canvas tag _var - -} {
upvar $_var var
$canvas itemconfigure $tag -text $var
}
package require Tk
set image_width [image width splash_image]
set image_height [image height splash_image]
set display_width [winfo screenwidth .]
set display_height [winfo screenheight .]
set x_position [expr {int(0.5*($display_width - $image_width))}]
set y_position [expr {int(0.5*($display_height - $image_height))}]
frame .root
canvas .root.canvas \
-width $image_width \
-height $image_height \
-borderwidth 0 \
-highlightthickness 0
.root.canvas create image \
[expr {$image_width / 2}] \
[expr {$image_height / 2}] \
-image splash_image
font create myFont {*}[font actual TkDefaultFont]
font configure myFont -size 10
.root.canvas create text \
10 \
55 \
-fill black \
-justify center \
-font myFont \
-tag vartext \
-anchor sw
trace variable status_text w \
[list canvas_text_update .root.canvas vartext]
set status_text "Initializing"
wm attributes . -transparentcolor magenta
.root.canvas configure -background magenta
pack .root
grid .root.canvas -column 0 -row 0 -columnspan 1 -rowspan 2
wm overrideredirect . 1
wm geometry . +${x_position}+${y_position}
wm attributes . -topmost 1
raise .�PNG

   IHDR  1   5   )���   sRGB ���   gAMA  ���a   	pHYs  �  ��o�d   �IDATx^��N���[B�BH��!{+	�%+�[���YYY�N�gBJf
�hSV"[��z�s=�y�s����~����z�ףs�q���s}�u�IYXXXD0,�YXXD4,�YXXD4,�YXXD4,�YXXD4,�YXXD4,�YXXD4,�YXXD4,�YXXD4,�YXXD4,�YXXD4,�YXXD4,�YXXD4,�YXXD4,�YXXD4,�Y�����5{�,5s���/�:g���㿪�g�V�f�T_��s�⿊�I�ҥKj�����E��{K��%��U_��?�]S�w�RS&MV/�{Q�Ы����jؐ!j�����W���sup��Z0o��o�z�g/ջGO5d�`5�\��?8W�Ɓ��⅋��K����h�B��ǟ8OQ��M���E�|�uｻD���w�9w�w�~+c7v�h���^�Oflx��Çe���ӎ9����N]�|��%<���35a�xy�0��Wջ���G��57����$L��e�,��/����J�"�ʘ>��͍��gΨ�+W�~c��a��W_~��<\Hݟ:�ʘ.�J��>�b�r��hl\�Aկ��z0Wn�&�*�]IU�dw�IG&-x̧6�_���w�V��wP�*�2��_ߗL���H�������ݖ��_U�O�v�F�.�䝙3<����>�z�3���U�l9u߽�|�u�1[�,꣏>�{��,>ظQ�l�\.PP���%���8c�Lݟ*�z�����?�,�A`ӦL�1}�5b�?n������մq�'GN�$Qbu�M7�[�q�ͷ���=�*�v|��s�?�n]���	nWOV��~��w�l�`<;���_�oɅ���mSY3f��Z����Y��5�Mb�W�僼 �,dRt~`�^��T�S�5\�������E�!���?w��իW�cƨ<9s�3x����'y����P�V-��?:OP��\m<���}��7ߔ�|�o�z(�~׻���_~�E�u�s���|��t�"@ ?��_�;�=��Su��8�/��z�uݦI�]�6Ҷ��ȶm-�k�h�"�.M^<����ՠ��������Z�Y��"�7/ qӎ��V�5՝��޵�uY������լ���&�3W%M|��מݻ���.Ο?C�%�6��9a�X7Y�(�R�|u��	�W%.R�4i�7����reˮ
�˯r��j%����Z![�>ܤ~/��kx�A�yF~MeJ�T�
��B�M�5yV�]����*W��b}���X;G}��^H��\��G�;�K�X��k���s���c�y�D�%PU+?�._�i!�ݳWU(S6�Py7��c�/w�J!u.i�;Ԭ�3������65e�d5i�B>��zKM���f����Ui劕�?Ŋ<�֮Y#�op��5Y|�v����M�e��_���v]��#����$�_����V����wϞ��,����<V����O�y�`�F��������F�$֫G!1�&V�+W��o�O��nУB8(<���6L}�ᇲ�mڴI�DդQ#_�|옱���*�&��u�~�5q{~����5J���A����9?i�b���ݯ�-��j����~X��=�[�f-5��7�bRĎN?.�3rTiӟRŊ���ǫiS��:&�~m���π
a�c��v,�E�EE�p��-j�w��/�#�w��Y�H�u:V�ڹSڇ�{��)�ؘ;g��m~�R�lx� ˕.�n�n�����/6i��O/D�ɺ5k�������H���$w	��( �M6TI&����_�~N�<)��mz^^}�笅AX$�kQ�vQB�/��> �͛>"�%BY�7��@����ҥ��(ZT}����1�d�������$w势�%�H�B*����7��w�_c+�����]5��ܾ��k��Z��5$Ș`A6~��Ī�� �d<n�ꫯ�r~���]��P�V�i)��$�w������A�Ϝ9e�a��	b����WP����~��=\�v�X�,r��h�_Ж�ڒ�bdq	yǹ��#>�:r��-ȪU+��q�E�zb�n`����A|Ǟ1��w�EbX7;Av����T�	�C,���n�����ꕫ�u˖b=�@&^�&%z�QcdH�
K����g�*Ϧys�R���+1�5�U�z>n$��p1K��*��OX���\�0�P�` �vb��+]&�7n� �:�m�Fƒ6�o�V4H���K�y�>d�j�\3	�s4j�@u����<i�(�۶����`��;V,tƜy%���S�3��p���ׇ9gcK�-m!�n�R��O�:5j���{�O�ow���>ۧ�g�"��Y����8u�X�-t�yq�.�:����~Y$ƌ��=�TU�	Y�Hr��Ö7K6�U��Wds;�k��Aj�+��G�̹2dT)?�خ��Y����ǴM�V����~C�A�n��������8 �ضU��,gƞd���}M����I�ukת�ݺ�ZO�PիTU-�5������I;?�Eb�?�E.� ��'.+�81H�G�[<�\H������*g�l1�*Q���0n���w�x���_c�m-�<����Ei�|����3���`��ϭX���2���}�|�sōNF���3���ݤ],$��&�-��/��o_��h�޽[���O�[n�{�f�$ւ�}�,Z,F,	+�r�G��wޥ���v�ةJ+��L�P�OvG�A!=�wW�=DI#�\i�;{��%֭��213��X�wޞH�˓GT�`т��d�K~�]!k�w@v��Ȯ�������vжl3���8#�ĺ��ݸACy&�1/�������t��8�Pƒ8�Ȼ�?�͘>]���������A+����	��C���]���f�h'�t0%�B2$0�ٜ�O�
h}v�s�ߦ_<�~ު��;{v	!���H��E�Y�DI��;�v�~Ȅ��Xp5C�X�ۊ����0@�ǐ�y�C~x�o�(�� �۲e��(ד6�ծ.���&����6}�-��xV��Oa��xX���e�z���r�J��#Y�J�S�r��l=笨S'O�e�Λ;W�dQ̡��H!q;#�k�BQY�L��ꐔ� '(;I��$/�o��lJ+.m��_��Ν�yF�x/%8^`1"�$[�=����{��U+�/��YI�������b��".XPbR��6�-UJ���٣�j��]~dk^�	2�hҰ�Z�Ǜ�Z�r�X:d�S'O)��b�2	˔����ĝߚ6M[��$c�^�;,GƝ��̞-�.w��=D&���H��#:� ?Ȯ�#EUm5!�eK���6q���H��~t~Vs��2�͛>5�+�-��]���$������C%F�k�.��ka�!�"1�AC(e�ڵ�_@P;w� + `��k�n]����޹:L�h��X-�J���r�����1�yG������uΆJ��Ƴ�'�V��ZiY�P^s@�������DY���Y?��>ӎ��w�:��T���{�9(-
�P�y+�&X�	�{-�U+WF�����cǎ9� �1���J��i�֝�;v��XS(Ө�#���<b.�FC@n�����='_|w\7��\\>w��2����Ƙ�?L�2EH9�&!�\����`QE��h�$����d�)��Î��B�U����ڂ�]:crdr��u�� ޙ3Gt�J���N��>b����ᎇ�<�s�g$SCVW=cO�}b�1�U�;dK�^y1�����H��%�%�y�� �l-`t��`�8W�x�X<��K���V͛;��1Cb(7�U����*V�z����t�Wt�Jo��C?�>���0�͑K���.^�cUG��)�>&�t��z����M$޼�(v���}c;XI\�F���@��0+�9O������$&���ʏ����V��ψ��/]&FLm��-2�,Z�B�.J�$᭷Ų�إ�|dҲrЉ�aڇ�Q���n���b��h)�-U�ҸA#uQˇ��Lyb\=�]���:g�qI?��SO��C�6�.\3,_��t@J��iR�+��>a�3��]�[�Є��{^[V'c߶ukuէ���1�4�+p�Y�˅�׋8IL���h������q=�=�u��
3V�D�5����Cz`ݮ��A�^}�p�Mz������A�=\*��ըZ=��B���C��:�� �˖�v�"���֋���`�-��@X JO�ڳ\���2�gVV/0��N�sɢ�e�� ���҈պ��,b��(#�X���``�=E
�ܥ�徔��H��z��0G(�_���Ty����(�7������@>^Y�Y�%/��%��cᄲ�	�#���7p��5Y|/֬^-mA�N� �9�k�#�;	�E�����b�R�,�k�������|�]��*jW^��֓OF��a�
S6�<4|��1\�Ib���r�"��i���_�|uj��a`p!PjV�&�k�<�R~�u�L0���Ṫ+m�'�F��YEb��P�cEB���Z�*v�;�׊�=O玝$�к�1#GK������\�x	鷐�n�Y���^���2�9�n�9J�P���\<�]�y������wi�˯D�b��2��ĒxJ���w�(��ʕ�A8�v��\t�t��A�[Q_O��jM�Ą^>\\^d�D�NYĀU��x�gK�t�$I��k�+�+ff�v8���J�"��xs�Jz���u`d�pk�Q��� 4��/Oޠ0aڃ�d��AFba�g���
˪_����d��[L��'��X2`�G�}��Y%A@��V���'	��I������6p�8Il��yZ�w&��P�`\R�(3D�_�0�v�}��K�YǸ���'gNy�Ab���@J��ø��^�C���ϝ#��^�I�y�I;��!l����[r#*��E��b�>M��n ��š���
��/�,J�kj��V�q���e�0����g�b@Y�7m���3�m��ڴl)� �HE=.*�b3��d�ʛO������4.s��!��%�J_��ح�ٞ=ί�e��&S�z�H��c�8g�Na4M�V.z9Ʋ�����Y��<!۵ !�%w��S�Lq���Mm���_�����0�ȿ｛�O,�W\X�@��'O���*����>��x/�q��'VV�A!��.L�Q��6�o�&fR�� �).��5���A%�F��m�\C�:�P�1L(�F!�(p���ٳ��m�}L*����XX�K�(�J��8���)}����}/��e�r�����en�0X�d�a玝��jvT@���h?���	S ;5�USmZ��s�N2�dV�/[VR�@�Sg!bȔ2 ?P��E�6s���w��x#�2��q�,x�1��V(�
��>�cƱ �;oH�����|���F�߀�4zI�"Ԟ\bux'�i��@�D] _>i��}Kg��������"�&��)�`<�(D�CHc��QJH�����8��2XX^&E�$����3�p~�q21+�b]��I�z�ի4q0c��b���D��'%K�c���
T��N��'p�Уk7Y�(c +f�)� )|/ 2���烂���������	�Y���F,��D��%�1p���zK2��~p!l\��@� ���P0l@���㞆B�c�������2)xq���Eq/	�P �μ@k�F�� 0v�N����,,,�m�"e���:�;�*�7X���S�����/�����~�۷�7#����J�s(�tkqS0�y�Q��=z�>��P+C�cB�g�z�"W�X�A�����������:��5<��H'�3����ÂY�dt�Y7'�?��|�ǫ�( ���eɐQ�{���a� *��p�磲M�����v��>�N���-2�=�*(m�ҹs�6�������.ˀ������ ¦�������oĜ���I*�ٞ��`�@�ċ}b���+����O!7.��E2$�sc�q���r�!'�F��1����i�OB��$�З�����c�1�$n�sB�� f&�A���r�9+4�P��O�b�
YyX��dq��^S�C��\ɠ�LAA����P��B�:H��<7PH\��31�CŷH���6c₱Z�5��L�Z!
	��]'j�%}2�^��,���\�%do�J1�M!(�nPR��"�{|�nA�_����^j�� �	�c50�������(�a��6n�@��WN�Ԁ�&�%_�8��s�ȳ���_�����+���q��E�5���N��Q�@!/q3�?SbK��;��Z�w��/늇��$�'�a�C�1.>���~�&�:S���U˕�%11w�'dX�l�@u��*(x��X��!I��dBQl2{��K$��Z�i�(B�4i�=��/�!N�R��w>_?eK����XW�+��l�a����g��⺹+�� �B����������:ϧ���-�!�7����xA� 8c`�O E���7����|�e�s���$
Ől�	��OQ(����������5ob�=��/�5_� 6d�X��c5��wa��k�Z�
���2��{�����I�
(�7�Gl��4�'���Ɉ$�'��h��z0�c�7׼��_���;�bj-�|ӎ��������i���0��,.Ǝ�����?aw�W�ŋ�y`����z�����3sb�`��3��n7����E+�g�1B#�r�BE�ݥKщ�����:��&����~i�x�|t֘��y�>��QRr�C�I�EY��Ă!$����i�Ȧ`��E����B��PC|��"�%6�W�b0|�0�1}zQ&�3�b�3�|TQE.���#�jN����3��l�Ʊ���	q����ІP�)�Z!7;w�{K�\p�ˌM���>����?�0��-�`7�͘�ZS��`z��fVt�s�ud�7e�{��BA����0��Dpy�Y�3�'����k$���wJ1ޜ8Q9��-�QV���������$�br,�&�O��SW,7,N�<��T��J�t�d����d�u�!�1���-�����(s�ز�ݛ�Ɗy��cQ:��Il�q�J�z���_�e�;慤.�^^�+�����@�e�֥aZw�k�Bg:w�+δI{�)��F�=3j��r�6����# ��L�R�G�\�֓��=�Ǣ��)�����s����-��yɝ� $����ұ��%Ww�2@��V�c:̀��ƽ K��������j�Vy��Q�&�g��r�.]ê'�lIKCX�G\A}~gգ���Ȗ9��T�����9G��������&a��Qd������l�/��8.+"{���&��v�/b��SKEU�p�5m*�▱��oo"_:���r�B�B��M ���J�����|�BAF�b�t���z<s	y��Ǫ#U�̟�bl%���?
��)�`QBap��Ί`�Rj�:憲 ���G	�?�c6�b��t��5h2
��/�����N2����@��s��K�,Z/���^�O�q�����O�f2]���/ǎCB�\��2/�U�[n�m�YH�����&��f�u;豧�=_��K8������<ƃ:2t�F�j��3�Ib�P�n<��a�s�b:LF�]Ly�G|B���V�"���� ���m)V!+�"��U�P�d�Ƞ`a��q����^�7���%4����o;ú���B@\���K_�+��K`���R�!�=F��Ç����>���~=d���d��CT�_qo�a�ڲy�e�MBT|]��G�x]މ{
$��C���e0�*A
��H���5��y��(�-�^Y���O�Պ�2B�����J -�'���"��dUÑ�g���"t�kt�+�Yq-}'6�s6l�}�W����l"���~>����؟��K�.K2C�^��ٗ���Wg/j�����y"�ϸ]�� $�YXX���$�(����#	��,,�������ў/�D,�YX��}�v��3&�ɰ$fa���i�$�D�)X�'R`I���?v�P��n����NF,�YX�� >"J66T�d$�����EDÒ���EDÒ���EDÒ���EDÒ���EDÒ���EDÒ���EDÒ���EDÒ���EC����
r%�[    IEND�B`�