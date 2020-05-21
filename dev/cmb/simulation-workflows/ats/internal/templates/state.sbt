<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <!-- TODO: field evaluators -->
    <AttDef Type="field-evaluator-base" BaseType="" Abstract="true" Version="0">
    </AttDef>

    <AttDef Type="richards water content" BaseType="field-evaluator-base" Version="0">
    </AttDef>

    <AttDef Type="capillary pressure, atmospheric gas over liquid" BaseType="field-evaluator-base" Version="0">
    </AttDef>

    <AttDef Type="viscosity" BaseType="field-evaluator-base" Version="0">
    </AttDef>

    <AttDef Type="effective_pressure" BaseType="field-evaluator-base" Version="0">
    </AttDef>

    <AttDef Type="independent variable" BaseType="field-evaluator-base" Version="0">
      <ItemDefinitions>
        <Void Name="constant in time" Optional="true" IsEnabledByDefault="true"></Void>
        <!-- name is the name of the attribute in the list -->
        <Double Name="value"></Double>
        <Component Name="region">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
          </Accepts>
        </Component>
        <!-- TODO: also need region components. one of: cell, face, boundary_face (can have just one or all three) -->
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="eos" BaseType="field-evaluator-base" Version="0">
      <!-- TODO add stuff -->
    </AttDef>

    <AttDef Type="molar fraction gas" BaseType="field-evaluator-base" Version="0">
    </AttDef>

    <AttDef Type="overland pressure water content" BaseType="field-evaluator-base" Version="0">
    </AttDef>

    <AttDef Type="ponded depth" BaseType="field-evaluator-base" Version="0">
    </AttDef>

    <AttDef Type="ponded depth bar" BaseType="field-evaluator-base" Version="0">
    </AttDef>



    <!-- ////////////////////////////////////////////////////////////// -->
    <!-- TODO: initial conditions / "atomic constants" -->
    <!-- NOTE: this section is called initial conditions, but its not that. ATS wants to change the anme of this section to "atomic constants" -->
    <!-- NOTE: these "initial conditions" might also need to be used by the PKs... so we may want to put into a seperate XML file -->

    <!-- Base class for initial conditions -->
    <AttDef Type="ic-base" BaseType="" Abstract="true" Version="0">
    </AttDef>

    <!-- Class for Initialization of constant scalars -->
    <AttDef Type="ic-const-scalar" BaseType="ic-base" Version="0">
      <ItemDefinitions>
        <Double Name="value"></Double>
      </ItemDefinitions>
    </AttDef>

    <!-- Class for Initialization of constant vectors -->
    <AttDef Type="ic-const-vector" BaseType="ic-base" Version="0">
      <ItemDefinitions>
        <!-- NOTE: this can be 2 or 3D, i.e. the list can be 2 elements or 3. For now, we keep as 3-->
        <Double Name="value" NumberOfRequiredValues="3"></Double>
      </ItemDefinitions>
    </AttDef>

    <!-- The rest don't seem needed for the demos. -->

    <!-- TODO: Initialization of scalar fields -->
    <!-- <AttDef Type="ic-scalar-field" BaseType="ic-base" Version="0">
      <ItemDefinitions>
      </ItemDefinitions>
    </AttDef> -->

    <!-- TODO: Initialization of tensor fields -->
    <!-- <AttDef Type="ic-tensor-field" BaseType="ic-base" Version="0">
      <ItemDefinitions>
      </ItemDefinitions>
    </AttDef> -->

    <!-- TODO: Initialization from a file -->
    <!-- <AttDef Type="ic-file" BaseType="ic-base" Version="0">
      <ItemDefinitions>
      </ItemDefinitions>
    </AttDef> -->


    <!-- ////////////////////////////////////////////////////////////// -->
    <!-- TODO: Boundary conditions? or is it just the other two sections? -->
  </Definitions>
</SMTK_AttributeResource>
