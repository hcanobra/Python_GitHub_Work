
import pandas as pd

html_string = """
<table>
<tr><td colspan="5" class="configHeader">Configuration Info</td><td colspan="14" class="auditHeader">Audit</td></tr><tr class="auditHeader"><td class="configHeader">Cell</td><td class="configHeader">Carr</td><td class="configHeader">Antenna</td><td class="configHeader">Az</td><td class="configHeader">MDT</td><td>Src</td><td>State</td><td>HW</td><td>Chan</td><td>BW</td><td>PCI</td><td>TAC</td><td>EAID</td><td width="18%">Radio</td><td>Power</td><td>AWS-3</td><td>#Tx</td><td>#Rx</td><td>EDT</td></tr>
					<tr class="f2Row"><td bgcolor="#FF9B9B"  rowspan="4">1</td><td rowspan="2">2</td><td rowspan="2" align="left">hbxx-3319ds-vtm_a__05edt</td><td rowspan="2"  >80</td><td rowspan="2"  >0</td><td align="right">Atoll</td><td>-</td><td>E</td><td>2050</td><td>-</td><td  >54</td><td  >3074</td><td>49035</td><td  align="center">8843</td><td  >40.00</td><td>-</td><td  >4</td><td  >4</td><td  >5.0</td></tr>
<tr class="f2Row" ><td align="right">Live</td><td></td><td>E</td><td>2050</td><td>20</td><td>54</td><td>3074</td><td>49035</td><td align="center">Radio 8843 B2 B66A</td><td>40.00</td><td></td><td>4</td><td>4</td><td  >5.0</td></tr>

					<tr class="f6Row"><td rowspan="2">6</td><td rowspan="2" align="left">hbxx-3319ds-vtm_a__05edt</td><td rowspan="2"  >80</td><td rowspan="2"  >0</td><td align="right">Atoll</td><td>-</td><td>E</td><td>67086</td><td>-</td><td  >54</td><td  >3074</td><td>49035</td><td  align="center">8843</td><td  >20.00</td><td>-</td><td  >4</td><td  >4</td><td  >5.0</td></tr>
<tr class="f6Row" ><td align="right">Live</td><td></td><td>E</td><td>67086</td><td>10</td><td>54</td><td>3074</td><td>49035</td><td align="center">Radio 8843 B2 B66A</td><td>20.00</td><td>UL/DL</td><td>4</td><td>4</td><td  >5.0</td></tr>

					<tr class="f2Row"><td bgcolor="#9B9BFF"  rowspan="4">2</td><td rowspan="2">2</td><td rowspan="2" align="left">hbxx-3319ds-vtm_a__03edt</td><td rowspan="2"  >220</td><td rowspan="2"  >0</td><td align="right">Atoll</td><td>-</td><td>E</td><td>2050</td><td>-</td><td  >55</td><td  >3074</td><td>49035</td><td  align="center">8843</td><td  >40.00</td><td>-</td><td  >4</td><td  >4</td><td  >3.0</td></tr>
<tr class="f2Row" ><td align="right">Live</td><td></td><td>E</td><td>2050</td><td>20</td><td>55</td><td>3074</td><td>49035</td><td align="center">Radio 8843 B2 B66A</td><td>40.00</td><td></td><td>4</td><td>4</td><td  >3.0</td></tr>

					<tr class="f6Row"><td rowspan="2">6</td><td rowspan="2" align="left">hbxx-3319ds-vtm_a__03edt</td><td rowspan="2"  >220</td><td rowspan="2"  >0</td><td align="right">Atoll</td><td>-</td><td>E</td><td>67086</td><td>-</td><td  >55</td><td  >3074</td><td>49035</td><td  align="center">8843</td><td  >20.00</td><td>-</td><td  >4</td><td  >4</td><td  >3.0</td></tr>
<tr class="f6Row" ><td align="right">Live</td><td></td><td>E</td><td>67086</td><td>10</td><td>55</td><td>3074</td><td>49035</td><td align="center">Radio 8843 B2 B66A</td><td>20.00</td><td>UL/DL</td><td>4</td><td>4</td><td  >3.0</td></tr>
</table>
				"""
    
dfs = pd.read_html(html_string)  
print (dfs)