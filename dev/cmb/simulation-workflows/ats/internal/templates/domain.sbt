<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>

    <!-- ATS mesh types -->
    <AttDef Type="mesh" Label="Mesh" BaseType="" Version="0">
      <ItemDefinitions>
        <!-- Where the mesh type is chosen: only one per simulation -->
        <String Name="mesh type">
          <ChildrenDefinitions>
            <Double Name="domain low coordinate" NumberOfRequiredValues="3">
              <DefaultValue>0.0</DefaultValue>
            </Double>
            <Double Name="domain high coordinate" NumberOfRequiredValues="3">
              <DefaultValue>1.0</DefaultValue>
            </Double>
            <Int Name="number of cells" NumberOfRequiredValues="3">
              <DefaultValue>1</DefaultValue>
              <RangeInfo>
                <Min Inclusive="true">1</Min>
              </RangeInfo>
            </Int>
            <File Name="file" ShouldExist="true"></File>
            <String Name="format">
              <DiscreteInfo>
                <Value Enum="MSTK">MSTK</Value>
                <Value Enum="Exodus II">Exodus II</Value>
              </DiscreteInfo>
            </String>
            <Component Name="surface sideset name">
              <Accepts>
                <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
              </Accepts>
            </Component>
            <String Name="subgrid region name">
              <!-- TODO: what is this?? -->
            </String>
            <String Name="entity kind">
              <DiscreteInfo DefaultIndex="0">
                <Value Enum="cell">0</Value>
                <Value Enum="face">1</Value>
                <Value Enum="node">2</Value>
              </DiscreteInfo>
            </String>
            <String Name="parent domain">
              <!-- TODO: what even is this? should it be pointing to something else? -->
              <DefaultValue>domain</DefaultValue>
            </String>
            <Void Name="flyweight mesh" Label="flyweight mesh" Optional="true" IsEnabledByDefault="false">
              <BriefDescription>NOT YET SUPPORTED. Allows a single mesh instead of one per entity.</BriefDescription>
            </Void>
          </ChildrenDefinitions>
          <!-- Here is where we list the options - they can adopt children from above -->
          <DiscreteInfo DefaultIndex="0">
            <Structure>
              <Value enum="generate mesh">generate mesh</Value>
              <Items>
                <Item>domain low coordinate</Item>
                <Item>domain high coordinate</Item>
                <Item>number of cells</Item>
              </Items>
            </Structure>
            <!-- "read mesh file" in exodusII or MSTK format -->
            <Structure>
              <Value enum="read mesh file">read mesh file</Value>
              <Items>
                <Item>file</Item>
                <Item>format</Item>
              </Items>
            </Structure>
            <!-- NOTE: "logical mesh" (no documentaion) -->
            <!-- TODO: "surface mesh" -->
            <Structure>
              <Value enum="surface">surface</Value>
              <Items>
                <!-- TODO: this can be `surface sideset name` or `surface sideset names`-->
                <!-- TODO: How do we deal with option to have one or many? -->
                <Item>surface sideset name</Item>
              </Items>
            </Structure>
            <!-- "subgrid mesh" -->
            <Structure>
              <Value enum="subgrid">subgrid</Value>
              <Items>
                <Item>subgrid region name</Item>
                <Item>entity kind</Item>
                <Item>parent domain</Item>
                <Item>flyweight mesh</Item>
              </Items>
            </Structure>
            <!-- TODO: "column mesh" -->
          </DiscreteInfo>
        </String>

        <!-- Specs for all mesh types below -->
        <Void Name="verify mesh" Label="verify the mesh" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>Perform a mesh audit</BriefDescription>
        </Void>
        <Void Name="deformable mesh" Label="deformable mesh" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>Will this mesh be deformed?</BriefDescription>
        </Void>
        <!-- “partitioner” [string] (zoltan_rcb) Method to partition the mesh. -->
        <String Name="partitioner">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="zoltan_rcb/map view">zoltan_rcb</Value>
            <Value Enum="METIS">metis</Value>
            <Value Enum="Zoltan">zoltan</Value>
          </DiscreteInfo>
        </String>
      </ItemDefinitions>
    </AttDef>


    <!-- Region subdomains -->
    <AttDef Type="region" Label="Region" Abstract="true" Version="0"></AttDef>
    <AttDef Type="region: all" BaseType="region"></AttDef>
    <AttDef Type="region: box" BaseType="region">
      <ItemDefinitions>
        <Double Name="low coordinate" NumberOfRequiredValues="3"></Double>
        <Double Name="high coordinate" NumberOfRequiredValues="3"></Double>
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="region: plane" BaseType="region">
      <ItemDefinitions>
        <Double Name="point" NumberOfRequiredValues="3"></Double>
        <Double Name="normal" NumberOfRequiredValues="3"></Double>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeResource>
