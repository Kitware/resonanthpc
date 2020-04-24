<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>

    <!-- ATS mesh types -->
    <AttDef Type="mesh" Label="Mesh" BaseType="" Version="0">
      <ItemDefinitions>
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
          </ChildrenDefinitions>
          <DiscreteInfo DefaultIndex="0">
            <Structure>
              <Value enum="generate mesh">generate mesh</Value>
              <Items>
                <Item>domain low coordinate</Item>
                <Item>domain high coordinate</Item>
                <Item>number of cells</Item>
              </Items>
            </Structure>
            <!-- TODO: "read mesh file" in exodusII or MSTK format -->
            <!-- TODO: "logical mesh" -->
            <!-- TODO: "surface mesh" -->
            <!-- TODO: "subgrid mesh" -->
            <!-- TODO: "column mesh" -->
          </DiscreteInfo>
        </String>
        <!-- TODO: “_mesh_type_ parameters” [_mesh_type_-spec] List of parameters associated with the type -->
        <Void Name="verify mesh" Label="verify the mesh" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>Perform a mesh audit</BriefDescription>
        </Void>
        <Void Name="deformable mesh" Label="deformable mesh" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>Will this mesh be deformed?</BriefDescription>
        </Void>
        <!-- TODO: “partitioner” [string] (zoltan_rcb) Method to partition the mesh. -->
            <!-- implement each of the choices for the partitioners -->
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
