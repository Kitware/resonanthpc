<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <AttDef Type="visualization driver" BaseType="" Version="0">
      <ItemDefinitions>
        <!-- TODO: file name "visdump_DOMAIN_data" -->
        <!-- TODO: how to set a default value? -->
        <File Name="file name base" ShouldExist="false"></File>

        <Void Name="dynamic mesh" Label="dynamic mesh" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>Write mesh data for every visualization dump; this facilitates visualizing deforming meshes.</BriefDescription>
        </Void>
        <String Name="time units">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="second">s</Value>
            <Value Enum="day">d</Value>
            <!-- NOTE: the year definition here is differnet than coordinator -->
            <Value Enum="year">yr 365</Value>
          </DiscreteInfo>
        </String>

        <!-- TODO: IOEvent spec for timing -->

      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeResource>
