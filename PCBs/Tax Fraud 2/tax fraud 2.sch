<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.6.2">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="50" name="dxf" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="53" name="tGND_GNDA" color="7" fill="9" visible="no" active="no"/>
<layer number="54" name="bGND_GNDA" color="1" fill="9" visible="no" active="no"/>
<layer number="56" name="wert" color="7" fill="1" visible="no" active="no"/>
<layer number="57" name="tCAD" color="7" fill="1" visible="no" active="no"/>
<layer number="59" name="tCarbon" color="7" fill="1" visible="no" active="no"/>
<layer number="60" name="bCarbon" color="7" fill="1" visible="no" active="no"/>
<layer number="88" name="SimResults" color="9" fill="1" visible="yes" active="yes"/>
<layer number="89" name="SimProbes" color="9" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
<layer number="99" name="SpiceOrder" color="7" fill="1" visible="no" active="no"/>
<layer number="100" name="Muster" color="7" fill="1" visible="yes" active="yes"/>
<layer number="101" name="Patch_Top" color="12" fill="4" visible="yes" active="yes"/>
<layer number="102" name="Mittellin" color="7" fill="1" visible="yes" active="yes"/>
<layer number="103" name="Stiffner" color="7" fill="1" visible="yes" active="yes"/>
<layer number="104" name="Name" color="7" fill="1" visible="yes" active="yes"/>
<layer number="105" name="Beschreib" color="7" fill="1" visible="yes" active="yes"/>
<layer number="106" name="BGA-Top" color="7" fill="1" visible="yes" active="yes"/>
<layer number="107" name="BD-Top" color="7" fill="1" visible="yes" active="yes"/>
<layer number="108" name="tBridges" color="7" fill="1" visible="yes" active="yes"/>
<layer number="109" name="tBPL" color="7" fill="1" visible="yes" active="yes"/>
<layer number="110" name="bBPL" color="7" fill="1" visible="yes" active="yes"/>
<layer number="111" name="MPL" color="7" fill="1" visible="yes" active="yes"/>
<layer number="112" name="tSilk" color="7" fill="1" visible="yes" active="yes"/>
<layer number="113" name="ReferenceLS" color="7" fill="1" visible="no" active="no"/>
<layer number="114" name="Badge_Outline" color="7" fill="1" visible="yes" active="yes"/>
<layer number="115" name="ReferenceISLANDS" color="7" fill="1" visible="yes" active="yes"/>
<layer number="116" name="Patch_BOT" color="9" fill="4" visible="yes" active="yes"/>
<layer number="117" name="BACKMAAT1" color="7" fill="1" visible="no" active="no"/>
<layer number="118" name="Rect_Pads" color="7" fill="1" visible="no" active="no"/>
<layer number="119" name="KAP_TEKEN" color="7" fill="1" visible="no" active="no"/>
<layer number="120" name="KAP_MAAT1" color="7" fill="1" visible="no" active="no"/>
<layer number="121" name="sName" color="7" fill="1" visible="yes" active="yes"/>
<layer number="122" name="_bPlace" color="7" fill="1" visible="yes" active="yes"/>
<layer number="123" name="tTestmark" color="7" fill="1" visible="no" active="yes"/>
<layer number="124" name="bTestmark" color="7" fill="1" visible="no" active="yes"/>
<layer number="125" name="_tNames" color="7" fill="1" visible="yes" active="yes"/>
<layer number="126" name="_bNames" color="7" fill="1" visible="yes" active="yes"/>
<layer number="127" name="_tValues" color="7" fill="1" visible="yes" active="yes"/>
<layer number="128" name="_bValues" color="7" fill="1" visible="yes" active="yes"/>
<layer number="129" name="Mask" color="7" fill="1" visible="yes" active="yes"/>
<layer number="130" name="SMDSTROOK" color="7" fill="1" visible="no" active="no"/>
<layer number="131" name="tAdjust" color="7" fill="1" visible="no" active="yes"/>
<layer number="132" name="bAdjust" color="7" fill="1" visible="no" active="yes"/>
<layer number="133" name="bottom_silk" color="7" fill="1" visible="no" active="no"/>
<layer number="134" name="silk_top" color="7" fill="1" visible="no" active="no"/>
<layer number="135" name="silk_bottom" color="7" fill="1" visible="no" active="no"/>
<layer number="136" name="silktop" color="7" fill="1" visible="yes" active="yes"/>
<layer number="137" name="silkbottom" color="7" fill="1" visible="yes" active="yes"/>
<layer number="138" name="mbTest" color="7" fill="1" visible="no" active="yes"/>
<layer number="139" name="mtKeepout" color="7" fill="1" visible="no" active="yes"/>
<layer number="140" name="mbKeepout" color="7" fill="1" visible="no" active="yes"/>
<layer number="141" name="mtRestrict" color="7" fill="1" visible="no" active="yes"/>
<layer number="142" name="mbRestrict" color="7" fill="1" visible="no" active="yes"/>
<layer number="143" name="mvRestrict" color="7" fill="1" visible="no" active="yes"/>
<layer number="144" name="Drill_legend" color="7" fill="1" visible="yes" active="yes"/>
<layer number="145" name="DrillLegend_01-16" color="7" fill="1" visible="yes" active="yes"/>
<layer number="146" name="DrillLegend_01-20" color="7" fill="1" visible="yes" active="yes"/>
<layer number="147" name="mMeasures" color="7" fill="1" visible="no" active="yes"/>
<layer number="148" name="mDocument" color="7" fill="1" visible="no" active="yes"/>
<layer number="149" name="mReference" color="7" fill="1" visible="no" active="yes"/>
<layer number="150" name="Notes" color="7" fill="1" visible="yes" active="yes"/>
<layer number="151" name="HeatSink" color="7" fill="1" visible="yes" active="yes"/>
<layer number="152" name="_bDocu" color="7" fill="1" visible="yes" active="yes"/>
<layer number="153" name="FabDoc1" color="6" fill="1" visible="no" active="no"/>
<layer number="154" name="FabDoc2" color="2" fill="1" visible="no" active="no"/>
<layer number="155" name="FabDoc3" color="7" fill="15" visible="no" active="no"/>
<layer number="166" name="AntennaArea" color="7" fill="1" visible="yes" active="yes"/>
<layer number="168" name="4mmHeightArea" color="7" fill="1" visible="yes" active="yes"/>
<layer number="191" name="mNets" color="7" fill="1" visible="no" active="yes"/>
<layer number="192" name="mBusses" color="7" fill="1" visible="no" active="yes"/>
<layer number="193" name="mPins" color="7" fill="1" visible="no" active="yes"/>
<layer number="194" name="mSymbols" color="7" fill="1" visible="no" active="yes"/>
<layer number="195" name="mNames" color="7" fill="1" visible="no" active="yes"/>
<layer number="196" name="mValues" color="7" fill="1" visible="no" active="yes"/>
<layer number="199" name="Contour" color="7" fill="1" visible="yes" active="yes"/>
<layer number="200" name="200bmp" color="1" fill="10" visible="yes" active="yes"/>
<layer number="201" name="201bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="202" name="202bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="203" name="203bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="204" name="204bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="205" name="205bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="206" name="206bmp" color="7" fill="10" visible="yes" active="yes"/>
<layer number="207" name="207bmp" color="8" fill="10" visible="yes" active="yes"/>
<layer number="208" name="208bmp" color="9" fill="10" visible="yes" active="yes"/>
<layer number="209" name="209bmp" color="7" fill="1" visible="no" active="yes"/>
<layer number="210" name="210bmp" color="7" fill="1" visible="no" active="yes"/>
<layer number="211" name="211bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="212" name="212bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="213" name="213bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="214" name="214bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="215" name="215bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="216" name="216bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="217" name="217bmp" color="18" fill="1" visible="no" active="no"/>
<layer number="218" name="218bmp" color="19" fill="1" visible="no" active="no"/>
<layer number="219" name="219bmp" color="20" fill="1" visible="no" active="no"/>
<layer number="220" name="220bmp" color="21" fill="1" visible="no" active="no"/>
<layer number="221" name="221bmp" color="22" fill="1" visible="no" active="no"/>
<layer number="222" name="222bmp" color="23" fill="1" visible="no" active="no"/>
<layer number="223" name="223bmp" color="24" fill="1" visible="no" active="no"/>
<layer number="224" name="224bmp" color="25" fill="1" visible="no" active="no"/>
<layer number="225" name="225bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="226" name="226bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="227" name="227bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="228" name="228bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="229" name="229bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="230" name="230bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="231" name="Eagle3D_PG1" color="7" fill="1" visible="no" active="no"/>
<layer number="232" name="Eagle3D_PG2" color="7" fill="1" visible="no" active="no"/>
<layer number="233" name="Eagle3D_PG3" color="7" fill="1" visible="no" active="no"/>
<layer number="248" name="Housing" color="7" fill="1" visible="yes" active="yes"/>
<layer number="249" name="Edge" color="7" fill="1" visible="yes" active="yes"/>
<layer number="250" name="Descript" color="7" fill="1" visible="yes" active="yes"/>
<layer number="251" name="SMDround" color="7" fill="1" visible="yes" active="yes"/>
<layer number="254" name="cooling" color="7" fill="1" visible="yes" active="yes"/>
<layer number="255" name="routoute" color="7" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="USB-C Adafruit USB4105-GF-A">
<packages>
<package name="GCT_USB4105-GF-A">
<wire x1="-4.32" y1="0.7" x2="-4.02" y2="0.4" width="0.0001" layer="46" curve="-90"/>
<wire x1="-4.02" y1="0.4" x2="-4.02" y2="-0.4" width="0.0001" layer="46"/>
<wire x1="-4.02" y1="-0.4" x2="-4.32" y2="-0.7" width="0.0001" layer="46" curve="-90"/>
<wire x1="-4.32" y1="-0.7" x2="-4.62" y2="-0.4" width="0.0001" layer="46" curve="-90"/>
<wire x1="-4.62" y1="-0.4" x2="-4.62" y2="0.4" width="0.0001" layer="46"/>
<wire x1="-4.62" y1="0.4" x2="-4.32" y2="0.7" width="0.0001" layer="46" curve="-90"/>
<wire x1="4.32" y1="0.7" x2="4.62" y2="0.4" width="0.0001" layer="46" curve="-90"/>
<wire x1="4.62" y1="0.4" x2="4.62" y2="-0.4" width="0.0001" layer="46"/>
<wire x1="4.62" y1="-0.4" x2="4.32" y2="-0.7" width="0.0001" layer="46" curve="-90"/>
<wire x1="4.32" y1="-0.7" x2="4.02" y2="-0.4" width="0.0001" layer="46" curve="-90"/>
<wire x1="4.02" y1="-0.4" x2="4.02" y2="0.4" width="0.0001" layer="46"/>
<wire x1="4.02" y1="0.4" x2="4.32" y2="0.7" width="0.0001" layer="46" curve="-90"/>
<wire x1="-4.32" y1="5.03" x2="-4.02" y2="4.73" width="0.0001" layer="46" curve="-90"/>
<wire x1="-4.02" y1="4.73" x2="-4.02" y2="3.63" width="0.0001" layer="46"/>
<wire x1="-4.02" y1="3.63" x2="-4.32" y2="3.33" width="0.0001" layer="46" curve="-90"/>
<wire x1="-4.32" y1="3.33" x2="-4.62" y2="3.63" width="0.0001" layer="46" curve="-90"/>
<wire x1="-4.62" y1="3.63" x2="-4.62" y2="4.73" width="0.0001" layer="46"/>
<wire x1="-4.62" y1="4.73" x2="-4.32" y2="5.03" width="0.0001" layer="46" curve="-90"/>
<wire x1="4.32" y1="5.03" x2="4.62" y2="4.73" width="0.0001" layer="46" curve="-90"/>
<wire x1="4.62" y1="4.73" x2="4.62" y2="3.63" width="0.0001" layer="46"/>
<wire x1="4.62" y1="3.63" x2="4.32" y2="3.33" width="0.0001" layer="46" curve="-90"/>
<wire x1="4.32" y1="3.33" x2="4.02" y2="3.63" width="0.0001" layer="46" curve="-90"/>
<wire x1="4.02" y1="3.63" x2="4.02" y2="4.73" width="0.0001" layer="46"/>
<wire x1="4.02" y1="4.73" x2="4.32" y2="5.03" width="0.0001" layer="46" curve="-90"/>
<wire x1="-4.79" y1="4.93" x2="4.79" y2="4.93" width="0.1" layer="51"/>
<wire x1="4.79" y1="4.93" x2="4.79" y2="-2.6" width="0.1" layer="51"/>
<wire x1="4.79" y1="-2.6" x2="-4.79" y2="-2.6" width="0.1" layer="51"/>
<wire x1="-4.79" y1="-2.6" x2="-4.79" y2="4.93" width="0.1" layer="51"/>
<wire x1="-4.79" y1="-1.32" x2="-4.79" y2="-2.6" width="0.2" layer="21"/>
<wire x1="-4.79" y1="-2.6" x2="4.79" y2="-2.6" width="0.2" layer="21"/>
<wire x1="4.79" y1="-2.6" x2="4.79" y2="-1.32" width="0.2" layer="21"/>
<wire x1="-5.1" y1="5.58" x2="-5.1" y2="-2.85" width="0.05" layer="39"/>
<wire x1="-5.1" y1="-2.85" x2="5.1" y2="-2.85" width="0.05" layer="39"/>
<wire x1="5.1" y1="-2.85" x2="5.1" y2="5.58" width="0.05" layer="39"/>
<wire x1="5.1" y1="5.58" x2="-5.1" y2="5.58" width="0.05" layer="39"/>
<text x="-5" y="7.5" size="1.27" layer="25">&gt;NAME</text>
<text x="-5" y="6" size="1.27" layer="27">&gt;VALUE</text>
<text x="5.4" y="-2.5" size="0.4064" layer="51">PCB EDGE</text>
<wire x1="4.8" y1="-2.6" x2="8.4" y2="-2.6" width="0.1" layer="51"/>
<wire x1="-4.79" y1="2.65" x2="-4.79" y2="1.4" width="0.2" layer="21"/>
<wire x1="4.79" y1="2.65" x2="4.79" y2="1.4" width="0.2" layer="21"/>
<pad name="S2" x="-4.32" y="0" drill="0.6" diameter="1" shape="long" rot="R90"/>
<pad name="S3" x="4.32" y="0" drill="0.6" diameter="1" shape="long" rot="R90"/>
<pad name="S1" x="-4.32" y="4.18" drill="0.6" diameter="1.05" shape="long" rot="R90"/>
<pad name="S4" x="4.32" y="4.18" drill="0.6" diameter="1.05" shape="long" rot="R90"/>
<hole x="2.89" y="3.68" drill="0.65"/>
<hole x="-2.89" y="3.68" drill="0.65"/>
<smd name="A1_B12" x="-3.2" y="4.755" dx="0.6" dy="1.15" layer="1"/>
<smd name="B1_A12" x="3.2" y="4.755" dx="0.6" dy="1.15" layer="1"/>
<smd name="A4_B9" x="-2.4" y="4.755" dx="0.6" dy="1.15" layer="1"/>
<smd name="B4_A9" x="2.4" y="4.755" dx="0.6" dy="1.15" layer="1"/>
<smd name="A7" x="0.25" y="4.755" dx="0.3" dy="1.15" layer="1"/>
<smd name="A6" x="-0.25" y="4.755" dx="0.3" dy="1.15" layer="1"/>
<smd name="B6" x="0.75" y="4.755" dx="0.3" dy="1.15" layer="1"/>
<smd name="A8" x="1.25" y="4.755" dx="0.3" dy="1.15" layer="1"/>
<smd name="B5" x="1.75" y="4.755" dx="0.3" dy="1.15" layer="1"/>
<smd name="B7" x="-0.75" y="4.755" dx="0.3" dy="1.15" layer="1"/>
<smd name="A5" x="-1.25" y="4.755" dx="0.3" dy="1.15" layer="1"/>
<smd name="B8" x="-1.75" y="4.755" dx="0.3" dy="1.15" layer="1"/>
</package>
</packages>
<symbols>
<symbol name="USB4105-GF-A">
<wire x1="-15.24" y1="12.7" x2="15.24" y2="12.7" width="0.254" layer="94"/>
<wire x1="15.24" y1="12.7" x2="15.24" y2="-12.7" width="0.254" layer="94"/>
<wire x1="15.24" y1="-12.7" x2="-15.24" y2="-12.7" width="0.254" layer="94"/>
<wire x1="-15.24" y1="-12.7" x2="-15.24" y2="12.7" width="0.254" layer="94"/>
<text x="-15.24" y="13.97" size="1.778" layer="95">&gt;NAME</text>
<text x="-15.24" y="-15.24" size="1.778" layer="96">&gt;VALUE</text>
<pin name="CC1" x="-20.32" y="5.08" length="middle"/>
<pin name="DP1" x="-20.32" y="2.54" length="middle"/>
<pin name="DN1" x="-20.32" y="0" length="middle"/>
<pin name="SBU1" x="-20.32" y="-2.54" length="middle"/>
<pin name="VBUS" x="20.32" y="10.16" length="middle" direction="pwr" rot="R180"/>
<pin name="CC2" x="20.32" y="5.08" length="middle" rot="R180"/>
<pin name="DP2" x="20.32" y="2.54" length="middle" rot="R180"/>
<pin name="DN2" x="20.32" y="0" length="middle" rot="R180"/>
<pin name="SBU2" x="20.32" y="-2.54" length="middle" rot="R180"/>
<pin name="GND" x="20.32" y="-7.62" length="middle" direction="pwr" rot="R180"/>
<pin name="SHELL_GND" x="20.32" y="-10.16" length="middle" direction="pwr" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="USB4105-GF-A" prefix="J">
<description>USB-C (USB TYPE-C) USB 2.0 Receptacle Connector 24 (16+8 Dummy) Position Surface Mount, Right Angle; Through Hole  </description>
<gates>
<gate name="G$1" symbol="USB4105-GF-A" x="0" y="0"/>
</gates>
<devices>
<device name="" package="GCT_USB4105-GF-A">
<connects>
<connect gate="G$1" pin="CC1" pad="A5"/>
<connect gate="G$1" pin="CC2" pad="B5"/>
<connect gate="G$1" pin="DN1" pad="A7"/>
<connect gate="G$1" pin="DN2" pad="B7"/>
<connect gate="G$1" pin="DP1" pad="A6"/>
<connect gate="G$1" pin="DP2" pad="B6"/>
<connect gate="G$1" pin="GND" pad="A1_B12 B1_A12"/>
<connect gate="G$1" pin="SBU1" pad="A8"/>
<connect gate="G$1" pin="SBU2" pad="B8"/>
<connect gate="G$1" pin="SHELL_GND" pad="S1 S2 S3 S4"/>
<connect gate="G$1" pin="VBUS" pad="A4_B9 B4_A9"/>
</connects>
<technologies>
<technology name="">
<attribute name="DESCRIPTION" value=" USB-C (USB TYPE-C) USB 2.0 Receptacle Connector 24 (16+8 Dummy) Position Surface Mount, Right Angle; Through Hole "/>
<attribute name="DIGI-KEY_PART_NUMBER" value="2073-USB4105-GF-ATR-ND"/>
<attribute name="MF" value="GCT"/>
<attribute name="MP" value="USB4105-GF-A"/>
<attribute name="PACKAGE" value="None"/>
<attribute name="PURCHASE-URL" value="https://pricing.snapeda.com/search/part/USB4105-GF-A/?ref=eda"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="TinyPICO_NANO_Eagle">
<packages>
<package name="TINYPICO-NANO-CONNECTOR">
<smd name="GND$4" x="17.9705" y="6.4135" dx="2.54" dy="2.54" layer="1" rot="R45" cream="no"/>
<rectangle x1="16.383" y1="6.6548" x2="17.145" y2="7.4168" layer="31" rot="R45"/>
<wire x1="0" y1="0" x2="0" y2="12.54" width="0.127" layer="51"/>
<wire x1="0" y1="12.54" x2="26.9875" y2="12.54" width="0.127" layer="51"/>
<wire x1="26.9875" y1="12.54" x2="26.9875" y2="0" width="0.127" layer="51"/>
<wire x1="26.9875" y1="0" x2="0" y2="0" width="0.127" layer="51"/>
<rectangle x1="23.495" y1="0.381" x2="26.67" y2="7.366" layer="51"/>
<smd name="IO23" x="4.7752" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="IO19" x="6.0452" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="IO18" x="7.3152" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="IO5" x="8.5852" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="IO22" x="9.8552" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="IO21" x="11.1252" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="IO0" x="12.3952" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="IO9" x="13.6652" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="RX" x="14.9352" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="TX" x="16.2052" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="IO39" x="17.4752" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="IO38" x="18.7452" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="IO37" x="20.0152" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="IO36" x="21.2852" y="0.1" dx="1" dy="1.2" layer="1"/>
<smd name="VBAT" x="4.7639" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO2" x="6.0339" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO4" x="7.3039" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO12" x="8.5739" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO13" x="9.8439" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO14" x="11.1139" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO15" x="12.3839" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO27" x="13.6539" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO26" x="14.9239" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO25" x="16.1939" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO32" x="17.4639" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO33" x="18.7339" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO34" x="20.0039" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="IO35" x="21.2739" y="12.44" dx="1" dy="1.2" layer="1"/>
<smd name="3V3" x="0.1" y="10.725" dx="1" dy="1.2" layer="1" rot="R270"/>
<smd name="EN" x="0.1" y="9.455" dx="1" dy="1.2" layer="1" rot="R270"/>
<smd name="D+" x="0.1" y="8.185" dx="1" dy="1.2" layer="1" rot="R270"/>
<smd name="D-" x="0.1" y="6.915" dx="1" dy="1.2" layer="1" rot="R270"/>
<smd name="5V" x="0.1" y="5.645" dx="1" dy="1.2" layer="1" rot="R270"/>
<smd name="RESET" x="0.1" y="4.375" dx="1" dy="1.2" layer="1" rot="R270"/>
<smd name="GND$1" x="0.1" y="3.105" dx="1" dy="1.2" layer="1" rot="R270"/>
<smd name="STAT" x="0.1" y="1.835" dx="1" dy="1.2" layer="1" rot="R270"/>
<smd name="GND$2" x="17.642840625" y="7.08151875" dx="3" dy="3" layer="1" rot="R45" cream="no"/>
<smd name="GND$3" x="19.43608125" y="6.746240625" dx="0.6604" dy="0.670559375" layer="1" cream="no"/>
<rectangle x1="17.3228" y1="7.62" x2="18.0848" y2="8.382" layer="31" rot="R45"/>
<rectangle x1="17.4244" y1="5.5372" x2="18.1864" y2="6.2992" layer="31" rot="R45"/>
<rectangle x1="18.4404" y1="6.5532" x2="19.2024" y2="7.3152" layer="31" rot="R45"/>
<wire x1="22.225" y1="8.89" x2="28.067" y2="8.89" width="0.127" layer="51"/>
<wire x1="28.067" y1="8.89" x2="28.067" y2="-1.27" width="0.127" layer="51"/>
<wire x1="28.067" y1="-1.27" x2="22.225" y2="-1.27" width="0.127" layer="51"/>
<wire x1="22.225" y1="-1.27" x2="22.225" y2="8.89" width="0.127" layer="51"/>
<text x="28.575" y="-1.27" size="0.762" layer="51">Antenna
GND
Clearance</text>
</package>
</packages>
<symbols>
<symbol name="TINYPICO-NANO-CONNECTOR">
<description>TinyPICO NANO Device Symbol&lt;br&gt;
https://www.tinypico.com/tinypico-nano</description>
<pin name="IO23" x="-18.034" y="-21.844" length="middle" rot="R90"/>
<pin name="IO19" x="-15.494" y="-21.844" length="middle" rot="R90"/>
<pin name="IO18" x="-12.954" y="-21.844" length="middle" rot="R90"/>
<pin name="IO5" x="-10.414" y="-21.844" length="middle" rot="R90"/>
<pin name="IO22" x="-7.874" y="-21.844" length="middle" rot="R90"/>
<pin name="IO21" x="-5.334" y="-21.844" length="middle" rot="R90"/>
<pin name="RX" x="2.286" y="-21.844" length="middle" rot="R90"/>
<pin name="TX" x="4.826" y="-21.844" length="middle" rot="R90"/>
<pin name="IO0" x="-2.794" y="-21.844" length="middle" rot="R90"/>
<pin name="IO32" x="7.366" y="21.336" length="middle" rot="R270"/>
<pin name="IO33" x="9.906" y="21.336" length="middle" rot="R270"/>
<pin name="RESET" x="-33.274" y="-4.064" length="middle"/>
<pin name="GND" x="-33.274" y="-6.604" length="middle" direction="pwr"/>
<pin name="5V" x="-33.274" y="-1.524" length="middle" direction="pwr"/>
<pin name="D-" x="-33.274" y="1.016" length="middle"/>
<pin name="D+" x="-33.274" y="3.556" length="middle"/>
<pin name="3V3" x="-33.274" y="8.636" length="middle" direction="pwr"/>
<pin name="VBAT" x="-18.034" y="21.336" length="middle" direction="pwr" rot="R270"/>
<pin name="IO2" x="-15.494" y="21.336" length="middle" rot="R270"/>
<pin name="IO4" x="-12.954" y="21.336" length="middle" rot="R270"/>
<pin name="IO12" x="-10.414" y="21.336" length="middle" rot="R270"/>
<pin name="IO13" x="-7.874" y="21.336" length="middle" rot="R270"/>
<pin name="IO14" x="-5.334" y="21.336" length="middle" rot="R270"/>
<pin name="IO15" x="-2.794" y="21.336" length="middle" rot="R270"/>
<pin name="IO27" x="-0.254" y="21.336" length="middle" rot="R270"/>
<pin name="IO26" x="2.286" y="21.336" length="middle" rot="R270"/>
<pin name="IO25" x="4.826" y="21.336" length="middle" rot="R270"/>
<wire x1="-28.194" y1="16.256" x2="-28.194" y2="-16.764" width="0.254" layer="94"/>
<wire x1="-28.194" y1="-16.764" x2="30.226" y2="-16.764" width="0.254" layer="94"/>
<wire x1="30.226" y1="-16.764" x2="30.226" y2="16.256" width="0.254" layer="94"/>
<wire x1="30.226" y1="16.256" x2="-28.194" y2="16.256" width="0.254" layer="94"/>
<text x="0" y="0" size="2.54" layer="94" align="center">TinyPICO NANO
CONNECTOR</text>
<pin name="IO34" x="12.446" y="21.336" length="middle" rot="R270"/>
<pin name="IO35" x="14.986" y="21.336" length="middle" rot="R270"/>
<pin name="GPIO9" x="-0.254" y="-21.844" length="middle" rot="R90"/>
<pin name="GPIO39" x="7.366" y="-21.844" length="middle" rot="R90"/>
<pin name="GPIO38" x="9.906" y="-21.844" length="middle" rot="R90"/>
<pin name="GPIO37" x="12.446" y="-21.844" length="middle" rot="R90"/>
<pin name="GPIO36" x="14.986" y="-21.844" length="middle" rot="R90"/>
<pin name="EN" x="-33.274" y="6.096" length="middle" direction="in"/>
<pin name="STAT" x="-33.274" y="-9.144" length="middle" direction="out"/>
<wire x1="20.066" y1="3.556" x2="20.066" y2="-14.224" width="0.254" layer="94"/>
<wire x1="20.066" y1="-14.224" x2="27.686" y2="-14.224" width="0.254" layer="94"/>
<wire x1="27.686" y1="-14.224" x2="27.686" y2="3.556" width="0.254" layer="94"/>
<wire x1="27.686" y1="3.556" x2="20.066" y2="3.556" width="0.254" layer="94"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="TINYPICO-NANO-CONNECTOR">
<description>TinyPICO NANO Footprint&lt;br&gt;
https://www.tinypico.com/tinypico-nano</description>
<gates>
<gate name="G$1" symbol="TINYPICO-NANO-CONNECTOR" x="2.54" y="-7.62"/>
</gates>
<devices>
<device name="" package="TINYPICO-NANO-CONNECTOR">
<connects>
<connect gate="G$1" pin="3V3" pad="3V3"/>
<connect gate="G$1" pin="5V" pad="5V"/>
<connect gate="G$1" pin="D+" pad="D+"/>
<connect gate="G$1" pin="D-" pad="D-"/>
<connect gate="G$1" pin="EN" pad="EN"/>
<connect gate="G$1" pin="GND" pad="GND$1 GND$2 GND$3 GND$4"/>
<connect gate="G$1" pin="GPIO36" pad="IO36"/>
<connect gate="G$1" pin="GPIO37" pad="IO37"/>
<connect gate="G$1" pin="GPIO38" pad="IO38"/>
<connect gate="G$1" pin="GPIO39" pad="IO39"/>
<connect gate="G$1" pin="GPIO9" pad="IO9"/>
<connect gate="G$1" pin="IO0" pad="IO0"/>
<connect gate="G$1" pin="IO12" pad="IO12"/>
<connect gate="G$1" pin="IO13" pad="IO13"/>
<connect gate="G$1" pin="IO14" pad="IO14"/>
<connect gate="G$1" pin="IO15" pad="IO15"/>
<connect gate="G$1" pin="IO18" pad="IO18"/>
<connect gate="G$1" pin="IO19" pad="IO19"/>
<connect gate="G$1" pin="IO2" pad="IO2"/>
<connect gate="G$1" pin="IO21" pad="IO21"/>
<connect gate="G$1" pin="IO22" pad="IO22"/>
<connect gate="G$1" pin="IO23" pad="IO23"/>
<connect gate="G$1" pin="IO25" pad="IO25"/>
<connect gate="G$1" pin="IO26" pad="IO26"/>
<connect gate="G$1" pin="IO27" pad="IO27"/>
<connect gate="G$1" pin="IO32" pad="IO32"/>
<connect gate="G$1" pin="IO33" pad="IO33"/>
<connect gate="G$1" pin="IO34" pad="IO34"/>
<connect gate="G$1" pin="IO35" pad="IO35"/>
<connect gate="G$1" pin="IO4" pad="IO4"/>
<connect gate="G$1" pin="IO5" pad="IO5"/>
<connect gate="G$1" pin="RESET" pad="RESET"/>
<connect gate="G$1" pin="RX" pad="RX"/>
<connect gate="G$1" pin="STAT" pad="STAT"/>
<connect gate="G$1" pin="TX" pad="TX"/>
<connect gate="G$1" pin="VBAT" pad="VBAT"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="resis CR1206-JW-512ELF">
<packages>
<package name="RESC3216X75N">
<text x="-2.33" y="-1.23" size="0.5" layer="27" align="top-left">&gt;VALUE</text>
<text x="-2.33" y="1.23" size="0.5" layer="25">&gt;NAME</text>
<wire x1="1.73" y1="-0.88" x2="-1.73" y2="-0.88" width="0.127" layer="51"/>
<wire x1="1.73" y1="0.88" x2="-1.73" y2="0.88" width="0.127" layer="51"/>
<wire x1="1.73" y1="-0.88" x2="1.73" y2="0.88" width="0.127" layer="51"/>
<wire x1="-1.73" y1="-0.88" x2="-1.73" y2="0.88" width="0.127" layer="51"/>
<wire x1="-0.59" y1="0.88" x2="0.59" y2="0.88" width="0.127" layer="21"/>
<wire x1="-0.59" y1="-0.88" x2="0.59" y2="-0.88" width="0.127" layer="21"/>
<wire x1="-2.331" y1="-1.135" x2="2.331" y2="-1.135" width="0.05" layer="39"/>
<wire x1="-2.331" y1="1.135" x2="2.331" y2="1.135" width="0.05" layer="39"/>
<wire x1="-2.331" y1="-1.135" x2="-2.331" y2="1.135" width="0.05" layer="39"/>
<wire x1="2.331" y1="-1.135" x2="2.331" y2="1.135" width="0.05" layer="39"/>
<smd name="1" x="-1.494" y="0" dx="1.17" dy="1.77" layer="1"/>
<smd name="2" x="1.494" y="0" dx="1.17" dy="1.77" layer="1"/>
</package>
</packages>
<symbols>
<symbol name="CR1206-JW-512ELF">
<wire x1="-5.08" y1="0" x2="-4.445" y2="1.905" width="0.254" layer="94"/>
<wire x1="-4.445" y1="1.905" x2="-3.175" y2="-1.905" width="0.254" layer="94"/>
<wire x1="-3.175" y1="-1.905" x2="-1.905" y2="1.905" width="0.254" layer="94"/>
<wire x1="-1.905" y1="1.905" x2="-0.635" y2="-1.905" width="0.254" layer="94"/>
<wire x1="-0.635" y1="-1.905" x2="0.635" y2="1.905" width="0.254" layer="94"/>
<wire x1="0.635" y1="1.905" x2="1.905" y2="-1.905" width="0.254" layer="94"/>
<wire x1="1.905" y1="-1.905" x2="3.175" y2="1.905" width="0.254" layer="94"/>
<wire x1="3.175" y1="1.905" x2="4.445" y2="-1.905" width="0.254" layer="94"/>
<wire x1="4.445" y1="-1.905" x2="5.08" y2="0" width="0.254" layer="94"/>
<text x="-7.624440625" y="2.54148125" size="2.54148125" layer="95">&gt;NAME</text>
<text x="-7.62996875" y="-5.086640625" size="2.54331875" layer="96">&gt;VALUE</text>
<pin name="1" x="-10.16" y="0" visible="off" length="middle" direction="pas"/>
<pin name="2" x="10.16" y="0" visible="off" length="middle" direction="pas" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="CR1206-JW-512ELF" prefix="R">
<description>RES SMD 5.1K OHM 5% 1/4W 1206 </description>
<gates>
<gate name="G$1" symbol="CR1206-JW-512ELF" x="0" y="0"/>
</gates>
<devices>
<device name="" package="RESC3216X75N">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name="">
<attribute name="DESCRIPTION" value=" 5.1 kOhms ±5% 0.25W, 1/4W Chip Resistor 1206 (3216 Metric) Moisture Resistant Thick Film "/>
<attribute name="DIGI-KEY_PART_NUMBER" value="118-CR1206-JW-512ELFTR-ND"/>
<attribute name="MF" value="Bourns"/>
<attribute name="MP" value="CR1206-JW-512ELF"/>
<attribute name="PACKAGE" value="3216 Bourns"/>
<attribute name="PURCHASE-URL" value="https://pricing.snapeda.com/search/part/CR1206-JW-512ELF/?ref=eda"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="buzzer">
<packages>
<package name="XDCR_AI-1223-TWT-12V-R">
<circle x="0" y="0" radius="6" width="0.127" layer="21"/>
<circle x="0" y="0" radius="6" width="0.127" layer="51"/>
<circle x="0" y="0" radius="6.25" width="0.05" layer="39"/>
<text x="-10.1741" y="8.2879" size="1.27" layer="25">&gt;NAME</text>
<text x="-10.1684" y="7.5977" size="1.27" layer="27" align="top-left">&gt;VALUE</text>
<wire x1="-0.635" y1="7.62" x2="0.635" y2="7.62" width="0.127" layer="21"/>
<wire x1="0" y1="8.255" x2="0" y2="6.985" width="0.127" layer="21"/>
<wire x1="-0.635" y1="-6.985" x2="0.635" y2="-6.985" width="0.127" layer="21"/>
<wire x1="-0.635" y1="7.62" x2="0.635" y2="7.62" width="0.127" layer="51"/>
<wire x1="0" y1="8.255" x2="0" y2="6.985" width="0.127" layer="51"/>
<wire x1="-0.635" y1="-6.985" x2="0.635" y2="-6.985" width="0.127" layer="51"/>
<pad name="P" x="0" y="3.8" drill="0.85"/>
<pad name="N" x="0" y="-3.8" drill="0.85"/>
</package>
</packages>
<symbols>
<symbol name="AI-1223-TWT-12V-R">
<wire x1="-3.175" y1="1.905" x2="-3.175" y2="-1.905" width="0.254" layer="94"/>
<wire x1="-3.175" y1="-1.905" x2="-2.54" y2="-1.905" width="0.254" layer="94"/>
<wire x1="0" y1="-1.905" x2="0" y2="1.905" width="0.254" layer="94"/>
<wire x1="-3.175" y1="1.905" x2="-2.54" y2="1.905" width="0.254" layer="94"/>
<wire x1="0" y1="-1.905" x2="2.54" y2="-5.08" width="0.254" layer="94"/>
<wire x1="2.54" y1="-5.08" x2="2.54" y2="5.08" width="0.254" layer="94"/>
<wire x1="0" y1="1.905" x2="2.54" y2="5.08" width="0.254" layer="94"/>
<wire x1="-2.54" y1="-2.54" x2="-2.54" y2="-1.905" width="0.1524" layer="94"/>
<wire x1="-2.54" y1="-1.905" x2="0" y2="-1.905" width="0.254" layer="94"/>
<wire x1="-2.54" y1="2.54" x2="-2.54" y2="1.905" width="0.1524" layer="94"/>
<wire x1="-2.54" y1="1.905" x2="0" y2="1.905" width="0.254" layer="94"/>
<text x="-1.27" y="6.35" size="1.778" layer="95">&gt;NAME</text>
<text x="-1.27" y="-8.255" size="1.778" layer="96">&gt;VALUE</text>
<text x="-5.08" y="2.54" size="1.778" layer="97">+</text>
<text x="-5.08" y="-5.08" size="1.778" layer="97">-</text>
<pin name="-" x="-2.54" y="-5.08" visible="off" length="short" direction="pas" rot="R90"/>
<pin name="+" x="-2.54" y="5.08" visible="off" length="short" direction="pas" rot="R270"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="AI-1223-TWT-12V-R" prefix="LS">
<description> &lt;a href="https://pricing.snapeda.com/parts/AI-1223-TWT-12V-R/PUI%20Audio%2C/view-part?ref=eda"&gt;Check availability&lt;/a&gt;</description>
<gates>
<gate name="G$1" symbol="AI-1223-TWT-12V-R" x="0" y="0"/>
</gates>
<devices>
<device name="" package="XDCR_AI-1223-TWT-12V-R">
<connects>
<connect gate="G$1" pin="+" pad="P"/>
<connect gate="G$1" pin="-" pad="N"/>
</connects>
<technologies>
<technology name="">
<attribute name="AVAILABILITY" value="In Stock"/>
<attribute name="DESCRIPTION" value=" ELECTRO-MECHANICAL AUDIO INDICATOR "/>
<attribute name="MF" value="PUI Audio,"/>
<attribute name="MP" value="AI-1223-TWT-12V-R"/>
<attribute name="PACKAGE" value="None"/>
<attribute name="PRICE" value="None"/>
<attribute name="PURCHASE-URL" value="https://pricing.snapeda.com/search/part/AI-1223-TWT-12V-R/?ref=eda"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="RFM95W-915S2">
<packages>
<package name="XCVR_RFM95W-915S2">
<wire x1="-8" y1="-8" x2="-8" y2="8" width="0.127" layer="51"/>
<wire x1="-8" y1="8" x2="8" y2="8" width="0.127" layer="51"/>
<wire x1="8" y1="8" x2="8" y2="-8" width="0.127" layer="51"/>
<wire x1="8" y1="-8" x2="-8" y2="-8" width="0.127" layer="51"/>
<wire x1="-8.25" y1="8.25" x2="8.25" y2="8.25" width="0.05" layer="39"/>
<wire x1="8.25" y1="8.25" x2="8.25" y2="7.95" width="0.05" layer="39"/>
<wire x1="8.25" y1="7.95" x2="9.45" y2="7.95" width="0.05" layer="39"/>
<wire x1="9.45" y1="7.95" x2="9.45" y2="-7.95" width="0.05" layer="39"/>
<wire x1="9.45" y1="-7.95" x2="8.25" y2="-7.95" width="0.05" layer="39"/>
<wire x1="8.25" y1="-7.95" x2="8.25" y2="-8.25" width="0.05" layer="39"/>
<wire x1="8.25" y1="-8.25" x2="-8.25" y2="-8.25" width="0.05" layer="39"/>
<wire x1="-8.25" y1="-8.25" x2="-8.25" y2="-7.95" width="0.05" layer="39"/>
<wire x1="-8.25" y1="-7.95" x2="-9.45" y2="-7.95" width="0.05" layer="39"/>
<wire x1="-9.45" y1="-7.95" x2="-9.45" y2="7.95" width="0.05" layer="39"/>
<wire x1="-9.45" y1="7.95" x2="-8.25" y2="7.95" width="0.05" layer="39"/>
<wire x1="-8.25" y1="7.95" x2="-8.25" y2="8.25" width="0.05" layer="39"/>
<text x="-9.805790625" y="8.905259375" size="1.27" layer="25">&gt;NAME</text>
<text x="-10.1033" y="-10.2033" size="1.27" layer="27">&gt;VALUE</text>
<circle x="-10.15" y="7.05" radius="0.1" width="0.2" layer="21"/>
<circle x="-10.15" y="7.05" radius="0.1" width="0.2" layer="51"/>
<wire x1="-8" y1="8" x2="8" y2="8" width="0.127" layer="21"/>
<wire x1="-8" y1="-8" x2="8" y2="-8" width="0.127" layer="21"/>
<smd name="1" x="-7.7" y="7" dx="3" dy="1.4" layer="1"/>
<smd name="2" x="-7.7" y="5" dx="3" dy="1.4" layer="1"/>
<smd name="3" x="-7.7" y="3" dx="3" dy="1.4" layer="1"/>
<smd name="4" x="-7.7" y="1" dx="3" dy="1.4" layer="1"/>
<smd name="5" x="-7.7" y="-1" dx="3" dy="1.4" layer="1"/>
<smd name="6" x="-7.7" y="-3" dx="3" dy="1.4" layer="1"/>
<smd name="7" x="-7.7" y="-5" dx="3" dy="1.4" layer="1"/>
<smd name="8" x="-7.7" y="-7" dx="3" dy="1.4" layer="1"/>
<smd name="9" x="7.7" y="-7" dx="3" dy="1.4" layer="1"/>
<smd name="10" x="7.7" y="-5" dx="3" dy="1.4" layer="1"/>
<smd name="11" x="7.7" y="-3" dx="3" dy="1.4" layer="1"/>
<smd name="12" x="7.7" y="-1" dx="3" dy="1.4" layer="1"/>
<smd name="13" x="7.7" y="1" dx="3" dy="1.4" layer="1"/>
<smd name="14" x="7.7" y="3" dx="3" dy="1.4" layer="1"/>
<smd name="15" x="7.7" y="5" dx="3" dy="1.4" layer="1"/>
<smd name="16" x="7.7" y="7" dx="3" dy="1.4" layer="1"/>
</package>
</packages>
<symbols>
<symbol name="RFM95W-915S2">
<wire x1="-12.7" y1="22.86" x2="-12.7" y2="-20.32" width="0.254" layer="94"/>
<wire x1="-12.7" y1="-20.32" x2="12.7" y2="-20.32" width="0.254" layer="94"/>
<wire x1="12.7" y1="-20.32" x2="12.7" y2="22.86" width="0.254" layer="94"/>
<wire x1="12.7" y1="22.86" x2="-12.7" y2="22.86" width="0.254" layer="94"/>
<text x="-12.7" y="22.86" size="1.778" layer="95">&gt;NAME</text>
<text x="-12.7" y="-22.86" size="1.778" layer="96">&gt;VALUE</text>
<pin name="GND" x="17.78" y="-17.78" length="middle" direction="pwr" rot="R180"/>
<pin name="MISO" x="-17.78" y="15.24" length="middle" direction="in"/>
<pin name="MOSI" x="17.78" y="15.24" length="middle" direction="out" rot="R180"/>
<pin name="SCK" x="-17.78" y="12.7" length="middle" direction="in" function="clk"/>
<pin name="NSS" x="-17.78" y="10.16" length="middle" direction="in"/>
<pin name="RESET" x="-17.78" y="5.08" length="middle"/>
<pin name="DIO5" x="-17.78" y="-12.7" length="middle"/>
<pin name="ANT" x="-17.78" y="2.54" length="middle"/>
<pin name="DIO3" x="-17.78" y="-7.62" length="middle"/>
<pin name="DIO4" x="-17.78" y="-10.16" length="middle"/>
<pin name="3.3V" x="17.78" y="20.32" length="middle" direction="pwr" rot="R180"/>
<pin name="DIO0" x="-17.78" y="0" length="middle"/>
<pin name="DIO1" x="-17.78" y="-2.54" length="middle"/>
<pin name="DIO2" x="-17.78" y="-5.08" length="middle"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="RFM95W-915S2" prefix="U">
<description>RFM95(W) - Low Power Long Range Transceiver Module V1.0 &lt;a href="https://pricing.snapeda.com/parts/RFM95W-915S2/RF%20Solutions/view-part?ref=eda"&gt;Check availability&lt;/a&gt;</description>
<gates>
<gate name="G$1" symbol="RFM95W-915S2" x="0" y="0"/>
</gates>
<devices>
<device name="" package="XCVR_RFM95W-915S2">
<connects>
<connect gate="G$1" pin="3.3V" pad="13"/>
<connect gate="G$1" pin="ANT" pad="9"/>
<connect gate="G$1" pin="DIO0" pad="14"/>
<connect gate="G$1" pin="DIO1" pad="15"/>
<connect gate="G$1" pin="DIO2" pad="16"/>
<connect gate="G$1" pin="DIO3" pad="11"/>
<connect gate="G$1" pin="DIO4" pad="12"/>
<connect gate="G$1" pin="DIO5" pad="7"/>
<connect gate="G$1" pin="GND" pad="1 8 10"/>
<connect gate="G$1" pin="MISO" pad="2"/>
<connect gate="G$1" pin="MOSI" pad="3"/>
<connect gate="G$1" pin="NSS" pad="5"/>
<connect gate="G$1" pin="RESET" pad="6"/>
<connect gate="G$1" pin="SCK" pad="4"/>
</connects>
<technologies>
<technology name="">
<attribute name="AVAILABILITY" value="In Stock"/>
<attribute name="DESCRIPTION" value=" 802.15.4 LoRa™ Transceiver Module 915MHz Antenna Not Included Surface Mount "/>
<attribute name="MF" value="RF Solutions"/>
<attribute name="MP" value="RFM95W-915S2"/>
<attribute name="PACKAGE" value="Non Standard RF Solutions"/>
<attribute name="PRICE" value="None"/>
<attribute name="PURCHASE-URL" value="https://pricing.snapeda.com/search/part/RFM95W-915S2/?ref=eda"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="adafruit" urn="urn:adsk.eagle:library:420">
<packages>
<package name="JST-PH-2-SMT-RA" urn="urn:adsk.eagle:footprint:6240046/1" library_version="2">
<description>2-Pin JST PH Series Right-Angle Connector (+/- for batteries)</description>
<wire x1="-4" y1="3" x2="4" y2="3" width="0.2032" layer="51"/>
<wire x1="4" y1="3" x2="4" y2="-4.5" width="0.2032" layer="51"/>
<wire x1="-4" y1="-4.5" x2="-4" y2="3" width="0.2032" layer="51"/>
<wire x1="3.2" y1="-2" x2="-3.2" y2="-2" width="0.2032" layer="51"/>
<wire x1="-3.2" y1="-2" x2="-3.2" y2="-4.5" width="0.2032" layer="51"/>
<wire x1="-3.2" y1="-4.5" x2="-4" y2="-4.5" width="0.2032" layer="51"/>
<wire x1="4" y1="-4.5" x2="3.2" y2="-4.5" width="0.2032" layer="51"/>
<wire x1="3.2" y1="-4.5" x2="3.2" y2="-2" width="0.2032" layer="51"/>
<wire x1="-2.25" y1="3" x2="2.25" y2="3" width="0.127" layer="21"/>
<wire x1="4" y1="-0.5" x2="4" y2="-4.5" width="0.127" layer="21"/>
<wire x1="4" y1="-4.5" x2="3.15" y2="-4.5" width="0.127" layer="21"/>
<wire x1="3.15" y1="-4.5" x2="3.15" y2="-2" width="0.127" layer="21"/>
<wire x1="3.15" y1="-2" x2="1.75" y2="-2" width="0.127" layer="21"/>
<wire x1="-1.75" y1="-2" x2="-3.15" y2="-2" width="0.127" layer="21"/>
<wire x1="-3.15" y1="-2" x2="-3.15" y2="-4.5" width="0.127" layer="21"/>
<wire x1="-3.15" y1="-4.5" x2="-4" y2="-4.5" width="0.127" layer="21"/>
<wire x1="-4" y1="-4.5" x2="-4" y2="-0.5" width="0.127" layer="21"/>
<smd name="2" x="-1" y="-3.7" dx="1" dy="4.6" layer="1"/>
<smd name="1" x="1" y="-3.7" dx="1" dy="4.6" layer="1"/>
<smd name="NC1" x="-3.4" y="1.5" dx="3.4" dy="1.6" layer="1" rot="R90"/>
<smd name="NC2" x="3.4" y="1.5" dx="3.4" dy="1.6" layer="1" rot="R90"/>
<text x="-2.54" y="3.81" size="1.27" layer="25" font="vector">&gt;Name</text>
<text x="-2.54" y="-7.62" size="1.27" layer="27" font="vector">&gt;Value</text>
<text x="2.286" y="-6.096" size="1.4224" layer="21" ratio="12">+</text>
<text x="-3.429" y="-6.096" size="1.4224" layer="21" ratio="12">-</text>
</package>
<package name="JST-PH-2-THM" urn="urn:adsk.eagle:footprint:6240047/1" library_version="2">
<description>4UCon #01528
http://www.4uconnector.com/online/object/4udrawing/01528.pdf</description>
<wire x1="3" y1="-1.7" x2="0.5" y2="-1.7" width="0.127" layer="21"/>
<wire x1="0.5" y1="-1.7" x2="0.5" y2="-2.2" width="0.127" layer="21"/>
<wire x1="0.5" y1="-2.2" x2="-0.5" y2="-2.2" width="0.127" layer="21"/>
<wire x1="-0.5" y1="-2.2" x2="-0.5" y2="-1.7" width="0.127" layer="21"/>
<wire x1="-0.5" y1="-1.7" x2="-3" y2="-1.7" width="0.127" layer="21"/>
<wire x1="-3" y1="-1.7" x2="-3" y2="2.8" width="0.127" layer="21"/>
<wire x1="-3" y1="2.8" x2="3" y2="2.8" width="0.127" layer="21"/>
<wire x1="3" y1="2.8" x2="3" y2="-1.7" width="0.127" layer="21"/>
<pad name="1" x="1" y="0" drill="0.8" diameter="1.4224" rot="R180"/>
<pad name="2" x="-1" y="0" drill="0.8" diameter="1.4224" rot="R180"/>
<text x="-2.8" y="-3.5" size="1.27" layer="25" font="vector">&gt;NAME</text>
<text x="4.064" y="0.762" size="1.27" layer="21" font="vector" rot="R180">+</text>
<text x="-3.302" y="0.762" size="1.27" layer="21" font="vector" rot="R180">-</text>
</package>
<package name="JST-PH-2-THM-RA" urn="urn:adsk.eagle:footprint:6240048/1" library_version="2">
<description>&lt;b&gt;S2B-PH-K-S&lt;/b&gt; 
&lt;p&gt;
JST PH 2-pin thru-home side entry</description>
<wire x1="-3" y1="6.3" x2="3" y2="6.3" width="0.127" layer="51"/>
<wire x1="3" y1="6.3" x2="3" y2="-1.4" width="0.127" layer="51"/>
<wire x1="-3" y1="-1.4" x2="-3" y2="6.3" width="0.127" layer="51"/>
<wire x1="-2.2" y1="-1.4" x2="-3" y2="-1.4" width="0.127" layer="51"/>
<wire x1="3" y1="-1.4" x2="2.2" y2="-1.4" width="0.127" layer="51"/>
<wire x1="-2.2" y1="-1.4" x2="-2.2" y2="-0.3" width="0.127" layer="21"/>
<wire x1="-2.2" y1="-0.3" x2="2.1" y2="-0.3" width="0.127" layer="21"/>
<wire x1="2.1" y1="-0.3" x2="2.1" y2="-1.4" width="0.127" layer="21"/>
<wire x1="2.1" y1="-1.4" x2="2.2" y2="-1.4" width="0.127" layer="21"/>
<wire x1="-0.3" y1="6.3" x2="-0.3" y2="3.4" width="0.127" layer="21"/>
<wire x1="-0.3" y1="3.4" x2="0.3" y2="3.4" width="0.127" layer="21"/>
<wire x1="0.3" y1="3.4" x2="0.3" y2="6.3" width="0.127" layer="21"/>
<pad name="2" x="-1" y="0" drill="0.8" diameter="1.4224"/>
<pad name="1" x="1" y="0" drill="0.8" diameter="1.4224"/>
<text x="-2.7" y="-3.8" size="1.27" layer="25" font="vector">&gt;NAME</text>
<text x="0.486" y="-2.096" size="1.4224" layer="21" ratio="12">+</text>
<text x="-1.429" y="-1.896" size="1.4224" layer="21" ratio="12">-</text>
</package>
<package name="JST-PH-2-SMT" urn="urn:adsk.eagle:footprint:6240117/1" library_version="2">
<wire x1="-4" y1="2.5" x2="4" y2="2.5" width="0.2032" layer="51"/>
<wire x1="4" y1="2.5" x2="4" y2="-2.5" width="0.2032" layer="51"/>
<wire x1="-4" y1="-2.5" x2="-4" y2="2.5" width="0.2032" layer="51"/>
<wire x1="4" y1="-2.5" x2="-4" y2="-2.5" width="0.2032" layer="51"/>
<wire x1="-2.25" y1="2.5" x2="2.25" y2="2.5" width="0.127" layer="21"/>
<wire x1="4" y1="-0.5" x2="4" y2="-2.5" width="0.127" layer="21"/>
<wire x1="4" y1="-2.5" x2="1.75" y2="-2.5" width="0.127" layer="21"/>
<wire x1="-1.75" y1="-2.5" x2="-4" y2="-2.5" width="0.127" layer="21"/>
<wire x1="-4" y1="-2.5" x2="-4" y2="-0.5" width="0.127" layer="21"/>
<smd name="1" x="-1" y="-1.8" dx="1" dy="5.5" layer="1"/>
<smd name="2" x="1" y="-1.8" dx="1" dy="5.5" layer="1"/>
<smd name="NC1" x="-3.4" y="0" dx="3.4" dy="1.6" layer="1" rot="R90"/>
<smd name="NC2" x="3.4" y="0" dx="3.4" dy="1.6" layer="1" rot="R90"/>
<text x="-2.54" y="3.81" size="1.27" layer="25" font="vector">&gt;Name</text>
<text x="-2.54" y="-7.62" size="1.27" layer="27" font="vector">&gt;Value</text>
<text x="-2.914" y="-6.096" size="1.4224" layer="21" ratio="12">+</text>
<text x="2.271" y="-6.096" size="1.4224" layer="21" ratio="12">-</text>
</package>
</packages>
<packages3d>
<package3d name="JST-PH-2-SMT-RA" urn="urn:adsk.eagle:package:6240692/1" type="box" library_version="2">
<description>2-Pin JST PH Series Right-Angle Connector (+/- for batteries)</description>
<packageinstances>
<packageinstance name="JST-PH-2-SMT-RA"/>
</packageinstances>
</package3d>
<package3d name="JST-PH-2-THM" urn="urn:adsk.eagle:package:6240693/1" type="box" library_version="2">
<description>4UCon #01528
http://www.4uconnector.com/online/object/4udrawing/01528.pdf</description>
<packageinstances>
<packageinstance name="JST-PH-2-THM"/>
</packageinstances>
</package3d>
<package3d name="JST-PH-2-THM-RA" urn="urn:adsk.eagle:package:6240694/1" type="box" library_version="2">
<description>&lt;b&gt;S2B-PH-K-S&lt;/b&gt; 
&lt;p&gt;
JST PH 2-pin thru-home side entry</description>
<packageinstances>
<packageinstance name="JST-PH-2-THM-RA"/>
</packageinstances>
</package3d>
<package3d name="JST-PH-2-SMT" urn="urn:adsk.eagle:package:6240763/1" type="box" library_version="2">
<packageinstances>
<packageinstance name="JST-PH-2-SMT"/>
</packageinstances>
</package3d>
</packages3d>
<symbols>
<symbol name="PINHD2" urn="urn:adsk.eagle:symbol:6239527/1" library_version="2">
<wire x1="-6.35" y1="-2.54" x2="1.27" y2="-2.54" width="0.4064" layer="94"/>
<wire x1="1.27" y1="-2.54" x2="1.27" y2="5.08" width="0.4064" layer="94"/>
<wire x1="1.27" y1="5.08" x2="-6.35" y2="5.08" width="0.4064" layer="94"/>
<wire x1="-6.35" y1="5.08" x2="-6.35" y2="-2.54" width="0.4064" layer="94"/>
<text x="-6.35" y="5.715" size="1.778" layer="95">&gt;NAME</text>
<text x="-6.35" y="-5.08" size="1.778" layer="96">&gt;VALUE</text>
<pin name="1" x="-2.54" y="2.54" visible="pad" length="short" direction="pas" function="dot"/>
<pin name="2" x="-2.54" y="0" visible="pad" length="short" direction="pas" function="dot"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="JST_2PIN" urn="urn:adsk.eagle:component:6241017/1" prefix="CN" uservalue="yes" library_version="2">
<description>&lt;b&gt;JST 2-Pin Connectors of various flavors&lt;/b&gt;

&lt;ul&gt;
&lt;li&gt;SMT-RA (S2B-PH-SM4) 4UConnector #17311&lt;/li&gt;
&lt;li&gt;SMT  (B2B-PH-SM4)&lt;/li&gt;
&lt;li&gt;THM-RA (S2B-PH)&lt;/li&gt;
&lt;li&gt;THM  (B2B-PH)&lt;/li&gt;
&lt;/ul&gt;</description>
<gates>
<gate name="G$1" symbol="PINHD2" x="2.54" y="0"/>
</gates>
<devices>
<device name="-SMT-RA" package="JST-PH-2-SMT-RA">
<connects>
<connect gate="G$1" pin="1" pad="2"/>
<connect gate="G$1" pin="2" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:6240692/1"/>
</package3dinstances>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="-THM" package="JST-PH-2-THM">
<connects>
<connect gate="G$1" pin="1" pad="2"/>
<connect gate="G$1" pin="2" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:6240693/1"/>
</package3dinstances>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="-THM-RA" package="JST-PH-2-THM-RA">
<connects>
<connect gate="G$1" pin="1" pad="2"/>
<connect gate="G$1" pin="2" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:6240694/1"/>
</package3dinstances>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="-SMT" package="JST-PH-2-SMT">
<connects>
<connect gate="G$1" pin="1" pad="2"/>
<connect gate="G$1" pin="2" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:6240763/1"/>
</package3dinstances>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="SparkFun-Connectors" urn="urn:adsk.eagle:library:513">
<description>&lt;h3&gt;SparkFun Connectors&lt;/h3&gt;
This library contains electrically-functional connectors. 
&lt;br&gt;
&lt;br&gt;
We've spent an enormous amount of time creating and checking these footprints and parts, but it is &lt;b&gt; the end user's responsibility&lt;/b&gt; to ensure correctness and suitablity for a given componet or application. 
&lt;br&gt;
&lt;br&gt;If you enjoy using this library, please buy one of our products at &lt;a href=" www.sparkfun.com"&gt;SparkFun.com&lt;/a&gt;.
&lt;br&gt;
&lt;br&gt;
&lt;b&gt;Licensing:&lt;/b&gt; Creative Commons ShareAlike 4.0 International - https://creativecommons.org/licenses/by-sa/4.0/ 
&lt;br&gt;
&lt;br&gt;
You are welcome to use this library for commercial purposes. For attribution, we ask that when you begin to sell your device using our footprint, you email us with a link to the product being sold. We want bragging rights that we helped (in a very small part) to create your 8th world wonder. We would like the opportunity to feature your device on our homepage.</description>
<packages>
<package name="1X04_1MM_RA" urn="urn:adsk.eagle:footprint:37714/1" library_version="1">
<description>&lt;h3&gt;SMD- 4 Pin Right Angle &lt;/h3&gt;
&lt;p&gt;Specifications:
&lt;ul&gt;&lt;li&gt;Pin count:4&lt;/li&gt;
&lt;li&gt;Pin pitch:0.1"&lt;/li&gt;
&lt;/ul&gt;&lt;/p&gt;
&lt;p&gt;Example device(s):
&lt;ul&gt;&lt;li&gt;CONN_04&lt;/li&gt;
&lt;/ul&gt;&lt;/p&gt;</description>
<wire x1="-1.5" y1="-4.6" x2="1.5" y2="-4.6" width="0.254" layer="21"/>
<wire x1="-3" y1="-2" x2="-3" y2="-0.35" width="0.254" layer="21"/>
<wire x1="2.25" y1="-0.35" x2="3" y2="-0.35" width="0.254" layer="21"/>
<wire x1="3" y1="-0.35" x2="3" y2="-2" width="0.254" layer="21"/>
<wire x1="-3" y1="-0.35" x2="-2.25" y2="-0.35" width="0.254" layer="21"/>
<circle x="-2.5" y="0.3" radius="0.1414" width="0.4" layer="21"/>
<smd name="NC2" x="-2.8" y="-3.675" dx="1.2" dy="2" layer="1"/>
<smd name="NC1" x="2.8" y="-3.675" dx="1.2" dy="2" layer="1"/>
<smd name="1" x="-1.5" y="0" dx="0.6" dy="1.35" layer="1"/>
<smd name="2" x="-0.5" y="0" dx="0.6" dy="1.35" layer="1"/>
<smd name="3" x="0.5" y="0" dx="0.6" dy="1.35" layer="1"/>
<smd name="4" x="1.5" y="0" dx="0.6" dy="1.35" layer="1"/>
<text x="-1.397" y="-2.159" size="0.6096" layer="25" font="vector" ratio="20">&gt;NAME</text>
<text x="-1.651" y="-3.302" size="0.6096" layer="27" font="vector" ratio="20">&gt;VALUE</text>
</package>
<package name="1X04_1MM_RA_STRESSRELIEF" urn="urn:adsk.eagle:footprint:37987/1" library_version="1">
<description>Qwiic connector with milled cutout. Sliding the cable into this slot prevents the cable from coming unplugged.</description>
<wire x1="-1.5" y1="-4.6" x2="1.5" y2="-4.6" width="0.254" layer="21"/>
<wire x1="-3" y1="-2" x2="-3" y2="-0.35" width="0.254" layer="21"/>
<wire x1="2.25" y1="-0.35" x2="3" y2="-0.35" width="0.254" layer="21"/>
<wire x1="3" y1="-0.35" x2="3" y2="-2" width="0.254" layer="21"/>
<wire x1="-3" y1="-0.35" x2="-2.25" y2="-0.35" width="0.254" layer="21"/>
<wire x1="-2" y1="-10.16" x2="-2" y2="-8" width="0.3048" layer="20"/>
<wire x1="-2" y1="-8" x2="4" y2="-8" width="0.3048" layer="20"/>
<wire x1="4" y1="-8" x2="4" y2="-6" width="0.3048" layer="20"/>
<wire x1="4" y1="-6" x2="-4" y2="-6" width="0.3048" layer="20"/>
<wire x1="-4" y1="-6" x2="-4" y2="-10.16" width="0.3048" layer="20"/>
<circle x="-2.5" y="0.3" radius="0.1414" width="0.4" layer="21"/>
<smd name="NC2" x="-2.8" y="-3.675" dx="1.2" dy="2" layer="1"/>
<smd name="NC1" x="2.8" y="-3.675" dx="1.2" dy="2" layer="1"/>
<smd name="1" x="-1.5" y="0" dx="0.6" dy="1.35" layer="1"/>
<smd name="2" x="-0.5" y="0" dx="0.6" dy="1.35" layer="1"/>
<smd name="3" x="0.5" y="0" dx="0.6" dy="1.35" layer="1"/>
<smd name="4" x="1.5" y="0" dx="0.6" dy="1.35" layer="1"/>
<text x="-1.397" y="-2.159" size="0.6096" layer="25" font="vector" ratio="20">&gt;NAME</text>
<text x="-1.651" y="-3.302" size="0.6096" layer="27" font="vector" ratio="20">&gt;VALUE</text>
<rectangle x1="-4" y1="-8" x2="4" y2="-6" layer="46"/>
<rectangle x1="-4" y1="-10" x2="-2" y2="-8" layer="46"/>
</package>
</packages>
<packages3d>
<package3d name="1X04_1MM_RA" urn="urn:adsk.eagle:package:38096/1" type="box" library_version="1">
<description>SMD- 4 Pin Right Angle 
Specifications:
Pin count:4
Pin pitch:0.1"

Example device(s):
CONN_04
</description>
<packageinstances>
<packageinstance name="1X04_1MM_RA"/>
</packageinstances>
</package3d>
<package3d name="1X04_1MM_RA_STRESSRELIEF" urn="urn:adsk.eagle:package:38303/1" type="box" library_version="1">
<description>Qwiic connector with milled cutout. Sliding the cable into this slot prevents the cable from coming unplugged.</description>
<packageinstances>
<packageinstance name="1X04_1MM_RA_STRESSRELIEF"/>
</packageinstances>
</package3d>
</packages3d>
<symbols>
<symbol name="I2C_STANDARD-1" urn="urn:adsk.eagle:symbol:37986/1" library_version="1">
<description>&lt;h3&gt;SparkFun I&lt;sup&gt;2&lt;/sup&gt;C Standard Pinout Header&lt;/h3&gt;
&lt;p&gt;SparkFun has standardized on a pinout for all I&lt;sup&gt;2&lt;/sup&gt;C based sensor breakouts.&lt;br&gt;</description>
<wire x1="3.81" y1="-5.08" x2="-5.08" y2="-5.08" width="0.4064" layer="94"/>
<wire x1="1.27" y1="2.54" x2="2.54" y2="2.54" width="0.6096" layer="94"/>
<wire x1="1.27" y1="0" x2="2.54" y2="0" width="0.6096" layer="94"/>
<wire x1="1.27" y1="-2.54" x2="2.54" y2="-2.54" width="0.6096" layer="94"/>
<wire x1="-5.08" y1="7.62" x2="-5.08" y2="-5.08" width="0.4064" layer="94"/>
<wire x1="3.81" y1="-5.08" x2="3.81" y2="7.62" width="0.4064" layer="94"/>
<wire x1="-5.08" y1="7.62" x2="3.81" y2="7.62" width="0.4064" layer="94"/>
<wire x1="1.27" y1="5.08" x2="2.54" y2="5.08" width="0.6096" layer="94"/>
<text x="-5.08" y="-5.334" size="1.778" layer="96" font="vector" align="top-left">&gt;VALUE</text>
<text x="-5.08" y="7.874" size="1.778" layer="95" font="vector">&gt;NAME</text>
<text x="-4.572" y="2.54" size="1.778" layer="94" font="vector" align="center-left">SDA</text>
<text x="-4.572" y="0" size="1.778" layer="94" font="vector" align="center-left">VCC</text>
<text x="-4.572" y="-2.54" size="1.778" layer="94" font="vector" align="center-left">GND</text>
<text x="-4.572" y="5.08" size="1.778" layer="94" font="vector" align="center-left">SCL</text>
<pin name="GND" x="7.62" y="-2.54" visible="pad" length="middle" direction="pwr" swaplevel="1" rot="R180"/>
<pin name="VCC" x="7.62" y="0" visible="pad" length="middle" direction="pwr" swaplevel="1" rot="R180"/>
<pin name="SDA" x="7.62" y="2.54" visible="pad" length="middle" direction="pas" swaplevel="1" rot="R180"/>
<pin name="SCL" x="7.62" y="5.08" visible="pad" length="middle" direction="pas" swaplevel="1" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="QWIIC_CONNECTOR" urn="urn:adsk.eagle:component:38395/1" prefix="J" uservalue="yes" library_version="1">
<description>&lt;h3&gt;SparkFun I&lt;sup&gt;2&lt;/sup&gt;C Standard Qwiic Connector&lt;/h3&gt;
An SMD 1mm pitch JST connector makes it easy and quick (get it? Qwiic?) to connect I&lt;sup&gt;2&lt;/sup&gt;C devices to each other. The &lt;a href=”http://www.sparkfun.com/qwiic”&gt;Qwiic system&lt;/a&gt; enables fast and solderless connection between popular platforms and various sensors and actuators.

&lt;br&gt;&lt;br&gt;

We carry &lt;a href=”https://www.sparkfun.com/products/14204”&gt;200mm&lt;/a&gt;, &lt;a href=”https://www.sparkfun.com/products/14205”&gt;100mm&lt;/a&gt;, &lt;a href=”https://www.sparkfun.com/products/14206”&gt;50mm&lt;/a&gt;, and &lt;a href=”https://www.sparkfun.com/products/14207”&gt;breadboard friendly&lt;/a&gt; Qwiic cables. We also offer &lt;a href=”https://www.sparkfun.com/products/14323”&gt;10 pcs strips&lt;/a&gt; the SMD connectors.</description>
<gates>
<gate name="J1" symbol="I2C_STANDARD-1" x="2.54" y="0"/>
</gates>
<devices>
<device name="JS-1MM" package="1X04_1MM_RA">
<connects>
<connect gate="J1" pin="GND" pad="1"/>
<connect gate="J1" pin="SCL" pad="4"/>
<connect gate="J1" pin="SDA" pad="3"/>
<connect gate="J1" pin="VCC" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:38096/1"/>
</package3dinstances>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="SR" package="1X04_1MM_RA_STRESSRELIEF">
<connects>
<connect gate="J1" pin="GND" pad="1"/>
<connect gate="J1" pin="SCL" pad="4"/>
<connect gate="J1" pin="SDA" pad="3"/>
<connect gate="J1" pin="VCC" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:38303/1"/>
</package3dinstances>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="J1" library="USB-C Adafruit USB4105-GF-A" deviceset="USB4105-GF-A" device=""/>
<part name="U$1" library="TinyPICO_NANO_Eagle" deviceset="TINYPICO-NANO-CONNECTOR" device=""/>
<part name="R1" library="resis CR1206-JW-512ELF" deviceset="CR1206-JW-512ELF" device=""/>
<part name="R2" library="resis CR1206-JW-512ELF" deviceset="CR1206-JW-512ELF" device=""/>
<part name="LS1" library="buzzer" deviceset="AI-1223-TWT-12V-R" device=""/>
<part name="U1" library="RFM95W-915S2" deviceset="RFM95W-915S2" device=""/>
<part name="CN1" library="adafruit" library_urn="urn:adsk.eagle:library:420" deviceset="JST_2PIN" device="-SMT-RA" package3d_urn="urn:adsk.eagle:package:6240692/1"/>
<part name="J2" library="SparkFun-Connectors" library_urn="urn:adsk.eagle:library:513" deviceset="QWIIC_CONNECTOR" device="JS-1MM" package3d_urn="urn:adsk.eagle:package:38096/1"/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="J1" gate="G$1" x="266.7" y="-25.4" smashed="yes">
<attribute name="NAME" x="251.46" y="-11.43" size="1.778" layer="95"/>
<attribute name="VALUE" x="251.46" y="-40.64" size="1.778" layer="96"/>
</instance>
<instance part="U$1" gate="G$1" x="114.3" y="68.58" smashed="yes" rot="R90"/>
<instance part="R1" gate="G$1" x="205.74" y="-12.7" smashed="yes">
<attribute name="NAME" x="198.115559375" y="-10.15851875" size="2.54148125" layer="95"/>
<attribute name="VALUE" x="198.11003125" y="-17.786640625" size="2.54331875" layer="96"/>
</instance>
<instance part="R2" gate="G$1" x="205.74" y="-27.94" smashed="yes">
<attribute name="NAME" x="198.115559375" y="-25.39851875" size="2.54148125" layer="95"/>
<attribute name="VALUE" x="198.11003125" y="-33.026640625" size="2.54331875" layer="96"/>
</instance>
<instance part="LS1" gate="G$1" x="162.56" y="10.16" smashed="yes" rot="R270">
<attribute name="NAME" x="168.91" y="11.43" size="1.778" layer="95" rot="R270"/>
<attribute name="VALUE" x="154.305" y="3.81" size="1.778" layer="96"/>
</instance>
<instance part="U1" gate="G$1" x="220.98" y="66.04" smashed="yes">
<attribute name="NAME" x="208.28" y="88.9" size="1.778" layer="95"/>
<attribute name="VALUE" x="208.28" y="43.18" size="1.778" layer="96"/>
</instance>
<instance part="CN1" gate="G$1" x="124.46" y="-17.78" smashed="yes">
<attribute name="NAME" x="118.11" y="-12.065" size="1.778" layer="95"/>
<attribute name="VALUE" x="118.11" y="-22.86" size="1.778" layer="96"/>
</instance>
<instance part="J2" gate="J1" x="96.52" y="-2.54" smashed="yes">
<attribute name="VALUE" x="91.44" y="-7.874" size="1.778" layer="96" font="vector" align="top-left"/>
<attribute name="NAME" x="91.44" y="5.334" size="1.778" layer="95" font="vector"/>
</instance>
</instances>
<busses>
</busses>
<nets>
<net name="N$1" class="0">
<segment>
<pinref part="R1" gate="G$1" pin="2"/>
<pinref part="J1" gate="G$1" pin="CC1"/>
<wire x1="215.9" y1="-12.7" x2="215.9" y2="-20.32" width="0.1524" layer="91"/>
<wire x1="215.9" y1="-20.32" x2="246.38" y2="-20.32" width="0.1524" layer="91"/>
</segment>
</net>
<net name="N$2" class="0">
<segment>
<pinref part="R2" gate="G$1" pin="2"/>
<wire x1="215.9" y1="-27.94" x2="236.22" y2="-27.94" width="0.1524" layer="91"/>
<wire x1="236.22" y1="-27.94" x2="236.22" y2="-60.96" width="0.1524" layer="91"/>
<wire x1="236.22" y1="-60.96" x2="307.34" y2="-60.96" width="0.1524" layer="91"/>
<wire x1="307.34" y1="-60.96" x2="307.34" y2="-25.4" width="0.1524" layer="91"/>
<wire x1="307.34" y1="-25.4" x2="294.64" y2="-25.4" width="0.1524" layer="91"/>
<wire x1="294.64" y1="-25.4" x2="294.64" y2="-20.32" width="0.1524" layer="91"/>
<pinref part="J1" gate="G$1" pin="CC2"/>
<wire x1="294.64" y1="-20.32" x2="287.02" y2="-20.32" width="0.1524" layer="91"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
<compatibility>
<note version="6.3" minversion="6.2.2" severity="warning">
Since Version 6.2.2 text objects can contain more than one line,
which will not be processed correctly with this version.
</note>
<note version="8.2" severity="warning">
Since Version 8.2, EAGLE supports online libraries. The ids
of those online libraries will not be understood (or retained)
with this version.
</note>
<note version="8.3" severity="warning">
Since Version 8.3, EAGLE supports URNs for individual library
assets (packages, symbols, and devices). The URNs of those assets
will not be understood (or retained) with this version.
</note>
<note version="8.3" severity="warning">
Since Version 8.3, EAGLE supports the association of 3D packages
with devices in libraries, schematics, and board files. Those 3D
packages will not be understood (or retained) with this version.
</note>
</compatibility>
</eagle>
