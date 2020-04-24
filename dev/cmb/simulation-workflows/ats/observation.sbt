<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <AttDef Type="observation-base" BaseType="" Version="0">
      <ItemDefinitions>

        <String Name="variable">
          <!-- TODO: ummm? should this be a drop down? It seems like available choices could depend on simulation -->
          <BriefDescription>any ATS variable used by any PK, e.g. “pressure” or “surface-water_content”</BriefDescription>
        </String>

        <!-- TODO: how to set a default value based on variable name? -->
        <File Name="observation output filename" ShouldExist="false"></File>

        <String Name="delimiter" DefauleValue=" "/>

        <String Name="region">
          <!-- TODO  should this be a drop down menu of available regions? -->
        </String>

        <String Name="location name">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="cell">0</Value>
            <Value Enum="face">1</Value>
            <Value Enum="node">2</Value>
          </DiscreteInfo>
          <BriefDescription>the mesh location of the thing to be measured, i.e. “cell”, “face”, or “node”</BriefDescription>
        </String>

        <String Name="functional">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="observation data: point">0</Value>
            <Value Enum="observation data: average">1</Value>
            <Value Enum="observation data: extensive integral">2</Value>
            <Value Enum="observation data: minimum">3</Value>
            <Value Enum="observation data: maximum">4</Value>
          </DiscreteInfo>
          <BriefDescription>the type of function to apply to the variable on the region</BriefDescription>
        </String>

        <Void Name="direction normalized flux" Label="direction normalized flux" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>For flux observations, dots the face-normal flux with a vector to ensure fluxes are integrated pointing the same direction.</BriefDescription>
        </Void>
        <!-- TODO: if that bool is true, add array of flux directions? -->

        <!-- TODO: add IOEvent -->


      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeResource>
