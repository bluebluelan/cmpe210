while true; do
    read -p "Demo what? a) extract icmp packet count b) extrace http packet count c)clear flow rule" yn
	echo ""
    case $yn in
        [Aa]* ) echo "curl http://192.168.56.102:8080/wm/headerExtract/icmpdst/json\n"; curl http://192.168.56.102:8080/wm/headerExtract/icmpdst/json | python -m json.tool; break;;
        [Bb]* ) echo "curl http://192.168.56.102:8080/wm/headerExtract/ipport/json\n"; curl http://192.168.56.102:8080/wm/headerExtract/ipport/json | python -m json.tool; break;;
		[Cc]* ) echo "curl http://192.168.56.102:8080/wm/staticflowpusher/clear/all/json\n"; curl http://192.168.56.102:8080/wm/staticflowpusher/clear/all/json | python -m json.tool; break;;
		[Xx]* ) exit;;
    esac
    clear
done